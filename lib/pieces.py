#!/bin/env python

from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.odict import odict
from vlib.utils import format_date, lazyproperty, validate_num_args

from piece_statuses import PieceStatuses
from piece_descriptions import PieceDescription
from piece_images import PieceImages
from piece_shows import PieceShows
from contacts import Contact
from transactions import Transactions

from dimensions import display_dimensions
import env

class Pieces(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'pieces')

    def getAll(self):
        '''Return list of Piece object'''
        sql = 'select id from pieces order by id'
        all = []
        for rec in self.db.query(sql):
            all.append(Piece(rec['id']))
        return all

    def list(self):
        header = ['id', 'name', 'created_year', 'status_description']
        rows = []
        for piece in self.getAll():
            rows.append([piece.id, piece.name, piece.created_year,
                         piece.status_description])
        return [[f for f in r] for r in rows]

class Piece(DataRecord):

    def __init__(self, id):
        '''Preside over a piece database record
           Id can be the pieces.id,
                         pieces.code or
                         <field>="<value>" pair
        '''
        self.db = db.getInstance()
        # code passed in?
        if not isinstance(id, (int)) and not id.isnumeric() and '=' not in id:
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
            return self.status
        else:
            data = {
                'status': self.status,
                'trans_date': self.trans_date,
                'owner_name': self.owner.fullname,
                'city': self.owner.city,
                'state': self.owner.state,
                }
            return '{status} {trans_date}: {owner_name}, {city}, {state}'.\
                format(**data)

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
            'add <name>',
            'add_edition <id|code> <csv_filepath>',
            'add_image <id|code> <img_filepath>',
            'list',
            'init_image_dirs <id|code',
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

        if cmd == 'list':
            return Pieces().list()

        elif cmd == 'init_image_dirs':
            validate_num_args('init_image_dirs', 1, args)
            filter = args.pop(0)
            return Piece(filter).initImageDirs()

        elif cmd == 'add_image':
            validate_num_args('load_image', 2, args)
            filter = args.pop(0)
            img_filepath = args.pop(0)
            return Piece(filter).addImage(img_filepath)

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
