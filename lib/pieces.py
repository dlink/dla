
from vlib import db
from vlib.datatable import DataTable
from vlib.odict import odict

class Pieces(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'pieces')

    def getAll(self):
        '''Return all records as a list of odicts'''
        return list(map(odict, self.get()))
