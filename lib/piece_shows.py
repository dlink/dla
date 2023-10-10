from vlib import db
from vlib.datatable import DataTable
from vlib.odict import odict

from shows import Show

class PieceShows:
    '''Preside over shows a given piece has been in'''

    def __init__(self, piece_id):
        self.piece_id = piece_id
        self.db = db.getInstance()
        self.spDt = DataTable(self.db, 'show_pieces')
        self.shows = self.getShows()

    def getShows(self):
        shows = []
        self.spDt.setFilters(f'piece_id = {self.piece_id}')
        for rec in self.spDt.getTable():
            rec = odict(rec)
            shows.append(Show(rec.show_id))
        return shows
