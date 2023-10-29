
from vweb.htmltable import HtmlTable
from vweb.html import div, h1, li, p, ul
from vlib.utils import is_int

from basepage import BasePage
from mediums import Medium
from pieces import Pieces
from thumbnails import Thumbnail

class GalleryPage(BasePage):

    panel_max_cols = 4

    def __init__(self, id):
        self.title = 'David Link '
        if is_int(id):
            self.title += f'Gallery {id}'
        else:
            self.title += f'{id}s'.title()
        BasePage.__init__(self, self.title)
        self.id = id
        self.pieces = Pieces()
        self.style_sheets.extend([
            self.versionize('css/gallery.css'),
            self.versionize('css/thumbnails.css')
        ])

    def getPageContent(self):
        medium = Medium(self.id)
        pieces = self.pieces.get({'medium_id': medium.id},
                                 medium.sort_order)

        # get thumbnails
        lis = ''
        for piece in pieces:
            if not piece.show_in_gallery:
                continue
            lis += li(Thumbnail(piece).html)

        if not lis:
            output = p(f'No pieces found for gallery "{self.id}".')
        else:
            output = ul(lis, class_='gallery__list')
        page_title = h1(medium.name)
        return div(
            h1(medium.name_plural) + \
            output, class_='gallery')

if __name__ == '__main__':
    HomePage().go()
