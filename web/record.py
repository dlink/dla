
import os

from vlib import db
from vlib import conf

#from vlib.datatable import DataTable
from vlib.datarecord import DataRecord

from vweb.htmlpage import HtmlPage
from vweb.htmltable import HtmlTable
from vweb.html import div, input, h1, span

# TO DO
# flesh out meta
# - hide
# - editable - max length
# - data type validate

meta = {
    'id': {'uneditable': 1},
    'code': {'hide': 1},
    'created': {'hide': 1},
    'dim_uom': {'uneditable': 1},
    'weight_uom': {'uneditable': 1},
    'r_created': {'uneditable': 1},
    'r_updated': {'uneditable': 1},
}

class Record(HtmlPage):

    def __init__(self, table_name, id):
        HtmlPage.__init__(self)
        
        self.table_name = table_name
        self.id = id
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        

        self.style_sheets.extend([
            self.versionize('css/record.css')
        ])

        #if id:
        self.dr = DataRecord(self.db, table_name, id)
        #else:
        #    self.dt = DataTable(self.db, table_name)

    def getHtmlContent(self):
        output = \
            self.getHeader() + \
            self.getBody()
        return div(output, id='page-container')


    def getHeader(self):
        return h1('Record Maintenance')

    def getBody(self):
        return self.displayFields()

    def displayFields(self):
        table = HtmlTable(class_='record-table')
        table.cellspacing = 10
        
        for col, value in self.dr.data.items():
            col_meta = meta.get(col, {})
            if col_meta.get('hide'):
                continue
            td_class = ''
            if col_meta.get('uneditable'):
                td_class = 'uneditable'
            else:
                value = input(name='name', value=value, size="100")

            table.addRow([col, str(value)])
            table.setCellClass(table.rownum, table.colnum, td_class)
        table.setColClass(1, 'row-header')

        return table.getTable()

    def versionize(self, file):
        timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir, file))
        return '/%s?v=%s' % (file, timestamp)
