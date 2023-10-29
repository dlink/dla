from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.utils import lazyproperty

from contacts import Contact

class Transactions(DataTable):
    '''Preside over art transactions'''

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'trans')

    def getAll(self):
        self.setFilters()
        self.setOrderBy(['trans_date desc', 'contact_id'])
        o = []
        for rec in self.getTable():
            o.append(Transaction(rec['id']))
        return o

    def getByPieceId(self, piece_id):
        self.setFilters(f'piece_id={piece_id}')
        results = self.getTable()
        if not results:
            return None
        return Transaction(results[0]['id'])

class Transaction(DataRecord):
    '''Provide over an art transaction'''

    def __init__(self, id):
        self.db = db.getInstance()
        DataRecord.__init__(self, self.db, 'trans', id)

    def __repr__(self):
        return f'Transaction:{self.id}:{self.trans_date}'

    @lazyproperty
    def contact(self):
        return Contact(self.contact_id)

    @lazyproperty
    def owner(self):
        return Contact(self.owner_id)

    @lazyproperty
    def piece_status(self):
        '''Convert sale type to piece_status'''
        if   self.type == 'sale'    : return 'Sold'
        elif self.type == 'gift'    : return 'Gifted'
        elif self.type == 'donation': return 'Donated'
        else                        : return self.type

    # Can not use due to circular reference
    # instead of
    #    p = transaction.piece
    # use
    #    from piece import Piece
    #    p = Piece(transaction.piece_id)
    #
    # @lazyproperty
    # def piece(self):
    #     return Piece(self.piece_id)
