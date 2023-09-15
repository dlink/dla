
from vweb.htmltable import HtmlTable

from basepage import BasePage
from pieces import Pieces
from thumbnails import Thumbnail

class HomePage(BasePage):

    panel_max_cols = 3

    def __init__(self):
        BasePage.__init__(self, 'DLA')
        self.pieces = Pieces()
        self.style_sheets.extend([
            self.versionize('css/pieces_panel.css'),
            self.versionize('css/thumbnails.css')
        ])

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
            row.append(Thumbnail(piece).html)
        if row:
            table.addRow(row)
        return table.getTable()

if __name__ == '__main__':
    HomePage().go()
