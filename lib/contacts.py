
from vlib import db
from vlib.datarecord import DataRecord

class Contact(DataRecord):

    def __init__(self, id):
        self.db = db.getInstance()
        DataRecord.__init__(self, self.db, 'contacts', id)

        # protect collectors privacy
        if not self.authorized:
            self.fullname = self.data.fullname = 'Private Collection'
