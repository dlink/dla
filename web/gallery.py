
from vweb.htmltable import HtmlTable
from vweb.html import div, li, p, ul
from vlib.utils import is_int

from basepage import BasePage
from pieces import Pieces
from thumbnails import Thumbnail

class GalleryPage(BasePage):

    panel_max_cols = 4

    def __init__(self, id):
        BasePage.__init__(self, 'DLA Gallery')
        self.id = id
        self.pieces = Pieces()
        self.style_sheets.extend([
            self.versionize('css/gallery.css'),
            self.versionize('css/thumbnails.css')
        ])

    def getPageContent(self):
        # medium.id or medium.code:
        if not is_int(self.id):
            medium = self.id
            pieces = self.pieces.getByMediumCode(medium)
        else:
            pieces = self.pieces.get({'medium_id': self.id})

        # get thumbnails
        lis = ''
        for piece in pieces:
            lis += li(Thumbnail(piece).html)

        if not lis:
            output = p(f'No pieces found for gallery "{self.id}".')
        else:
            output = ul(lis, class_='gallery__list')
        return div(output, class_='gallery')

if __name__ == '__main__':
    HomePage().go()
