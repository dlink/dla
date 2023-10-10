from vlib import db
from vlib.datarecord import DataRecord
from vlib.utils import lazyproperty

from contacts import Contact

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
