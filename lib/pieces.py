#!/bin/env python

from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord, DataRecordNotFound
from vlib.odict import odict
from vlib.utils import format_date, is_int, lazyproperty, validate_num_args

from piece_statuses import PieceStatuses
from piece_descriptions import PieceDescription
from piece_images import PieceImages
from piece_shows import PieceShows
from mediums import Medium
from contacts import Contact
from transactions import Transactions

from dimensions import display_dimensions
import env

class Pieces(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'pieces')

    def get(self, filters={}):
        '''Return list of Piece object'''
        self.setFilters(filters)
        self.setOrderBy(['created_year desc', 'sort_order', 'id desc'])
        all = []
        for rec in self.getTable():
            all.append(Piece(rec['id']))
        return all

    def getByMediumCode(self, medium_code):
        try:
            medium = Medium(medium_code)
        except DataRecordNotFound as e:
            return []
        return self.get({'medium_id': medium.id})

    def list(self):
        header = ['id', 'name', 'created_year', 'status_description']
        rows = []
        for piece in self.get():
            rows.append([piece.id, piece.name, piece.medium.name,
                         piece.created_year, piece.status_description])
        return [[f for f in r] for r in rows]

class Piece(DataRecord):

    def __init__(self, id):
        '''Preside over a piece database record
           Id can be the pieces.id,
                         pieces.code, (edition=1 implied)
                         pieces.code '-' pieces.edition
                         <field>="<value>" pair
        '''
        self.db = db.getInstance()
        if not is_int(id) and '=' not in id:
            code = id
            edition = 1
            if '-' in code:
                code, edition = code.split('-')[0:2 ]
            id=f"code='{code}' and edition = {edition}"

        DataRecord.__init__(self, self.db, 'pieces', id)
        self.data.status = self.status
        self.data.dimensions = self.dimensions
        self.data.description_html = self.description_html
        self.data.status_description = self.status_description
        self.data.edition_info = self.edition_info

    def __repr__(self):
        return f'Piece:({self.name}-{self.edition})'

    def initImageDirs(self):
        return self.images.initImageDirs()

    def addImage(self, img_filepath):
        return self.images.addImage(img_filepath)

    def updateImages(self):
        return self.images.updateImages()

    @lazyproperty
    def status(self):
        return PieceStatuses().getName(self.status_id)

    @lazyproperty
    def images(self):
        return PieceImages(self)

    @lazyproperty
    def medium(self):
        return Medium(self.medium_id)

    @lazyproperty
    def dimensions(self):
        dimensions = ''
        if self.length and self.width and self.height:
            dimensions = display_dimensions(self.length,self.width,self.height)
        return dimensions

    @lazyproperty
    def edition_info(self):
        if self.edition > 1:
            return f'(Edition {self.edition})'
        return ''

    @lazyproperty
    def description_html(self):
        return PieceDescription(self).description_html

    @lazyproperty
    def owner(self):
        return Contact(self.owner_id) if self.owner_id else None

    @lazyproperty
    def trans_date(self):
        created = Transactions().getFinalTransactionDate(self.id)
        return format_date(created) if created else ''

    @lazyproperty
    def status_description(self):
        if not self.owner_id:
            status = self.status
        else:
            data = {
                'status': self.status,
                'trans_date': self.trans_date,
                'owner_name': self.owner.fullname,
                'city': self.owner.city,
                'state': self.owner.state,
                }
            status= '{status} {trans_date}: {owner_name}, {city}, {state}'.\
                format(**data)
        if self.status not in ('Available', 'In Show'):
            status += ' (Can be remade)'
        return status

    @lazyproperty
    def shows(self):
        return PieceShows(self.id).shows

    @lazyproperty
    def versions(self):
        return self._getVersions()

    def _getVersions(self, visited=None):
        if visited is None:
            visited = set()
        _versions = []

        # Check if the piece has already been visited
        if self.id in visited:
            return []

        # Mark the current piece as visited
        visited.add(self.id)

        # get editions based on the same code but different edition
        self.setFilters(f'code="{self.code}"')
        for rec in self.getTable():
            if rec['edition'] != self.edition:
                other_edition = Piece(rec['id'])
                if other_edition.id not in visited:
                    _versions.append(other_edition)
                _versions.extend(other_edition._getVersions(visited))

        # get orig_piece if it exists and its versions
        if self.orig_piece:
            if self.orig_piece.id not in visited:
                _versions.append(self.orig_piece)
            _versions.extend(self.orig_piece._getVersions(visited))

        # if orig_piece, get copies
        self.setFilters(f'orig_piece_id={self.id}')
        for rec in self.getTable():
            copy_piece = Piece(rec['id'])
            if copy_piece.id not in visited:
                _versions.append(copy_piece)
            _versions.extend(copy_piece._getVersions(visited))

        # remove this piece
        _versions = [v for v in _versions if v.id != self.id]

        return _versions

    @lazyproperty
    def orig_piece(self):
        if self.orig_piece_id:
            return Piece(self.orig_piece_id)
        return None

    def show(self):
        from copy import copy
        data2 = copy(self.data)
        del data2.description_html
        data2.versions = self.versions
        data2.orig_piece = self.orig_piece
        return data2

class PiecesCLIError(Exception): pass

class PiecesCLI(object):
    '''Command line interface to the Product Class
       Used for discovery
    '''

    def __init__(self):
        self.env = env.getInstance()

    def run(self):
        '''Set up Command Line (CLI) commands and options
           for Pieces Module
        '''
        from cli import CLI
        commands = [
            'add_image <id|code[-edition]> <img_filepath>',
            'update_images <id|code[-edition]>',
            'list',
            'images <id|code[-edition]>',
            'show <id|code[-edition]>',
            'shows <id|code[-edition]>',
        ]
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
        '''
        args = list(args)
        cmd = args.pop(0)

        if self.cli.hasoption.get('v'):
            self.env.verbose = 1


        if cmd == 'add_image':
            validate_num_args('add_image', 2, args)
            filter = args.pop(0)
            img_filepath = args.pop(0)
            return Piece(filter).addImage(img_filepath)

        elif cmd == 'update_images':
            validate_num_args('update_images', 1, args)
            filter = args.pop(0)
            return Piece(filter).updateImages()

        elif cmd == 'list':
            return Pieces().list()

        elif cmd == 'images':
            validate_num_args('images', 1, args)
            filter = args.pop(0)
            return Piece(filter).images.filepaths

        elif cmd == 'show':
            validate_num_args('shows', 1, args)
            filter = args.pop(0)
            return Piece(filter).show()

        else:
            raise PiecesCLIError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    PiecesCLI().run()
    # p = Piece(74)
    # for v in p.versions:
    #     print(f'{v.name}-{v.edition}')
