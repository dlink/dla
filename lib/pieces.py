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
                         pieces.code or
                         <field>="<value>" pair
        '''
        self.db = db.getInstance()
        if not is_int(id) and '=' not in id:
            code = id
            id=f'code="{code}"'
        DataRecord.__init__(self, self.db, 'pieces', id)
        self.data.status = self.status
        self.data.dimensions = self.dimensions
        self.data.description_html = self.description_html
        self.data.status_description = self.status_description

    def initImageDirs(self):
        return self.images.initImageDirs()

    def addImage(self, img_filepath):
        return self.images.addImage(img_filepath)

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
            'add_image <id|code> <img_filepath>',
            'list',
            'images <id|code>',
            'shows <id|code>',
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
            validate_num_args('load_image', 2, args)
            filter = args.pop(0)
            img_filepath = args.pop(0)
            return Piece(filter).addImage(img_filepath)

        elif cmd == 'list':
            return Pieces().list()

        elif cmd == 'images':
            validate_num_args('images', 1, args)
            filter = args.pop(0)
            return Piece(filter).images.filepaths

        elif cmd == 'shows':
            validate_num_args('shows', 1, args)
            filter = args.pop(0)
            return [s.info for s in Piece(filter).shows]

        else:
            raise PiecesCLIError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    PiecesCLI().run()
