
from vweb.htmltable import HtmlTable
from vweb.html import div, li, ul

from basepage import BasePage
from pieces import Pieces
from thumbnails import Thumbnail

class HomePage(BasePage):

    panel_max_cols = 4

    def __init__(self):
        BasePage.__init__(self, 'DLA')
        self.pieces = Pieces()
        self.style_sheets.extend([
            self.versionize('css/gallery.css'),
            self.versionize('css/thumbnails.css')
        ])

    def getPageContent(self):
        lis = ''
        for piece in self.pieces.getAll():
            lis += li(Thumbnail(piece).html)

        return div(ul(lis, class_='gallery__list'), class_='gallery')

if __name__ == '__main__':
    HomePage().go()
