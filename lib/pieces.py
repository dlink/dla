
from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.odict import odict
from vlib.utils import lazyproperty

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
            dimensions = f'{self.length} x {self.width} x {self.height}'
            if self.dim_uom:
                dimensions = f'{dimensions} {self.dim_uom}'
        return dimensions
