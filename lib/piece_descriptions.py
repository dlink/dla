
from mistune import markdown

from vlib import db
from vlib.datatable import DataTable
from vlib.odict import odict
from vlib.utils import lazyproperty

class PieceDescription:

    def __init__(self, piece):
        self.piece = piece
        self.db = db.getInstance()
        self.pieceDescriptionsDt = DataTable(self.db, 'piece_descriptions')
        self.pieceDescriptionsDt.setFilters({'piece_id': self.piece.id})
        results = self.pieceDescriptionsDt.getTable()
        if not results:
            self.data = odict({'description': None,
                               'notes': None})
        else:
            self.data = odict(results[0])

    @lazyproperty
    def description(self): return self.data.description

    @lazyproperty
    def description_html(self): return markdown(self.data.description)

    @lazyproperty
    def notes(self): return self.data.notes
