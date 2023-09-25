
from vweb.htmltable import HtmlTable
from vweb.html import img, p

from basepage import BasePage
from pieces import Piece
from thumbnails import Thumbnail

class PiecePage(BasePage):

    panel_max_cols = 4

    def __init__(self):
        BasePage.__init__(self, 'Piece Page')
        self.piece = None
        #self.style_sheets.extend([
        #    self.versionize('css/pieces_panel.css'),
        #    self.versionize('css/thumbnails.css')
        #])

    def process(self):
        BasePage.process(self)

        # get piece
        id = self.form.get('id', '')
        if id:
            self.piece = Piece(id)
        
    def getPageContent(self):
        if not self.piece:
            return p('No art piece selected.  Use piece_id=nn')
        table = HtmlTable(class_='piece')
        for image_url in self.piece.images.tiny_urls:
            cell = img(src=f'{image_url}')
            table.addRow([cell])
        return table.getTable()

if __name__ == '__main__':
    PiecePage().go()
