
from vweb.htmltable import HtmlTable
from vweb.html import img

from basepage import BasePage
from pieces import Pieces

class HomePage(BasePage):

    panel_max_cols = 3

    def __init__(self):
        BasePage.__init__(self, 'DLA')
        self.pieces = Pieces()

    def getPageContent(self):
        table = HtmlTable(class_='pieces-panel')
        selected_pieces = self.pieces.getAll()
        row = []
        done = 0
        i = 0
        for piece in selected_pieces:
            i += 1
            if i % self.panel_max_cols == 1 and i != 1:
                table.addRow(row)
                row = []
            pic = img(src=piece.images.urls[0],
                      width='200px')

            row.append(f'[{piece.id}:{piece.name} {pic}]')
        if row:
            table.addRow(row)
        return table.getTable()

if __name__ == '__main__':
    HomePage().go()
