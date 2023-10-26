from vlib import db
from vlib.datatable import DataTable
from vlib.datarecord import DataRecord
from vlib.utils import is_int, lazyproperty

from contacts import Contact

class Shows(DataTable):

    def __init__(self):
        self.db = db.getInstance()
        DataTable.__init__(self, self.db, 'shows')

    def getAll(self):
        self.setFilters()
        self.setOrderBy('start_date desc')
        o = []
        for rec in self.getTable():
            o.append(Show(rec['id']))
        return o


class Show(DataRecord):
    '''Provide over art shows pieces have been in'''

    def __init__(self, id):
        self.db = db.getInstance()
        if not is_int(id) and '=' not in id:
            code = id
            id = f"code='{code}'"
        DataRecord.__init__(self, self.db, 'shows', id)

    @lazyproperty
    def contact(self):
        if self.contact_id:
            return Contact(self.contact_id)
        return None

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
