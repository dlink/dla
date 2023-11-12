
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
        self.medium = Medium(self.id)
        self.style_sheets.extend([
            self.versionize('css/gallery.css'),
            self.versionize('css/thumbnails.css')
        ])

    def getPieces(self):
        pieces = self.pieces.get({'medium_id': self.medium.id},
                                 self.medium.sort_order)
        pieces_list = []
        for piece in pieces:
            if not piece.show_in_gallery:
                continue
            pieces_list.append(piece)
        return pieces_list

    def getPageContent(self):

        # get thumbnails
        lis = ''
        for piece in self.getPieces():
            lis += li(Thumbnail(piece).html)

        if not lis:
            output = p(f'No pieces found for gallery "{self.id}".')
        else:
            output = ul(lis, class_='gallery__list')
        page_title = h1(self.medium.name)
        return div(
            h1(self.medium.name_plural) + \
            output, class_='gallery')

if __name__ == '__main__':
    HomePage().go()
