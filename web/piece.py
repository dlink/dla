
from vlib.datarecord import DataRecordNotFound

from vweb.htmltable import HtmlTable
from vweb.html import div, img, p, span

from basepage import BasePage
from pieces import Piece
from thumbnails import Thumbnail

class PiecePage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'Piece Page')
        self.piece = None
        self.piece_not_found = 0
        self.style_sheets.extend([
            self.versionize('css/main.css'),
            self.versionize('css/piece.css'),
        ])

    def process(self):
        BasePage.process(self)

        # get piece
        self.id = id = self.form.get('id', '')
        if id:
            try:
                self.piece = Piece(id)
            except DataRecordNotFound as e:
                self.piece_not_found = 1

    def getPageContent(self):
        if self.piece_not_found:
            return p(f'Piece "{self.id}" not found.')
        if not self.piece:
            return p('No art piece selected.  Use piece_id=nn')

        return div(
            self.getPicMenu() + \
            self.getMainPic() + \
            self.getPieceDescription(),
            id='pic-container')

    def getPicMenu(self):
        return ''
        o = ''
        if len(self.piece.images.tiny_urls) > 1:
            for image_url in self.piece.images.tiny_urls:
                pic = img(src=f'{image_url}')
                o += span(pic)
        return div(o, id='piece-pic-menu')

    def getMainPic(self):
        o = img(src=self.piece.images.display_urls[0])
        return div(o, id='main-pic')

    def getPieceDescription(self):
        template = self.getTemplate('piece_description.html')
        return template.format(**self.piece.data)

if __name__ == '__main__':
    PiecePage().go()
