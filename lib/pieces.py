#!/bin/env python

from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.odict import odict
from vlib.utils import lazyproperty, validate_num_args

from piece_images import PieceImages

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

    @lazyproperty
    def images(self):
        return PieceImages(self)

    @lazyproperty
    def dimensions(self):
        dimensions = ''
        if self.length and self.width and self.height:
            dimensions = \
                f'{dimf(self.length)} x {dimf(self.width)} x ' \
                f'{dimf(self.height)}'
            if self.dim_uom:
                dimensions = f'{dimensions} {self.dim_uom}'
        return dimensions

def dimf(dim):
    '''format Decimal dimension number
         match these:
           1.00 -> 1
           1.25 -> 1-1/4
           1.50 -> 1-1/2
           1.75 -> 1-3/4
         else:
           1.30 -> 1.30
    '''
    dim_int = int(dim)
    if dim_int == dim:
        return dim_int
    elif dim_int + 0.25 == dim:
        return f'{dim_int}-1/4'
    elif dim_int + 0.5 == dim:
        return f'{dim_int}-1/2'
    elif dim_int + 0.75 == dim:
        return f'{dim_int}-3/4'
    return dim

class PiecesCLIError(Exception): pass

class PiecesCLI(object):
    '''Command line interface to the Product Class
       Used for discovery
    '''

    def run(self):
        '''Set up Command Line (CLI) commands and options
           for Pieces Module
        '''
        from cli import CLI
        commands = ['images <id|code>']
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
        '''
        args = list(args)
        cmd = args.pop(0)

        if cmd == 'images':
            validate_num_args('images', 1, args)
            filter = args.pop(0)
            return Piece(filter).images.filepaths
        else:
            raise PiecesCLIError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    PiecesCLI().run()
