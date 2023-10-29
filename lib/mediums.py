
from vlib import db
from vlib.datarecord import DataRecord
from vlib.utils import is_int

class Medium(DataRecord):

    def __init__(self, id):
        '''Id can be id or code'''
        self.db = db.getInstance()
        if not is_int(id) and '=' not in id:
            code = id
            id=f'code="{code}"'
        DataRecord.__init__(self, self.db, 'mediums', id)

    def __repr__(self):
        return f'Medium:{self.id}:{self.code}'

    @property
    def name_plural(self):
        return self.name + 's'

    @property
    def sort_order(self):
        if self.code == 'painting':
            return ['sort_order']
        else:
            return None
