
from vlib.datatable import DataTable
from vlib import db

class Transactions(object):

    def __init__(self):
        self.db = db.getInstance()

    def getFinalTransactionDate(self, piece_id):
        sql = \
            'select max(created) as created ' \
            'from transactions where piece_id = %s'
        results = self.db.query(sql, params=(piece_id,))
        if results:
            return results[0]['created']
        else:
            return ''
