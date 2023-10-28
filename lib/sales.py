from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.utils import is_int, lazyproperty

from contacts import Contact
from pieces import Piece

class Sales(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'sales')

    def getAll(self):
        self.setFilters()
        self.setOrderBy('sale_date desc')
        o = []
        for rec in self.getTable():
            o.append(Sale(rec['id']))
        return o


class Sale(DataRecord):
    '''Provide over art sales'''

    def __init__(self, id):
        self.db = db.getInstance()
        DataRecord.__init__(self, self.db, 'sales', id)

    @lazyproperty
    def contact(self):
        return Contact(self.contact_id)

    @lazyproperty
    def owner(self):
        return Contact(self.owner_id)

    @lazyproperty
    def piece(self):
        return Piece(self.piece_id)
