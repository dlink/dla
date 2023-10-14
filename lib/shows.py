from vlib import db
from vlib.datarecord import DataRecord
from vlib.utils import lazyproperty

from contacts import Contact
#from show_pieces import ShowPieces

class Show(DataRecord):
    '''Provide over art shows pieces have been in'''

    def __init__(self, id):
        self.db = db.getInstance()
        DataRecord.__init__(self, self.db, 'shows', id)

    @lazyproperty
    def contact(self):
        return Contact(self.contact_id)

    @lazyproperty
    def info(self):
        return \
            f'"{self.name}" at ' \
            f'{self.contact.company_name}, ' \
            f'{self.contact.city}, {self.contact.state}, ' \
            f'{self.start_date}-{self.end_date}'

    # hack - to avoid circular ref
    # it might be better to put lazyproperties into a base class
    @lazyproperty
    def piece_ids(self):
        from vlib.datatable import DataTable
        from vlib.odict import odict
        self.spDt = DataTable(self.db, 'show_pieces')
        piece_ids = []
        self.spDt.setFilters(f'show_id = {self.id}')
        for rec in self.spDt.getTable():
            rec = odict(rec)
            #pieces.append(Pieces(rec.pieces_id))
            piece_ids.append(rec.piece_id)
        return piece_ids
