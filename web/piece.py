
from vlib.datarecord import DataRecordNotFound

from vweb.htmltable import HtmlTable
from vweb.html import div, img, input, li, p, span, ul

from basepage import BasePage
from pieces import Piece
from thumbnails import Thumbnail

class PiecePage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'Piece Page')
        self.piece = None
        self.piece_not_found = 0
        self.javascript_src.extend(['js/piece.js'])
        self.style_sheets.extend([
            self.versionize('css/main.css'),
            self.versionize('css/piece.css'),
            self.versionize('css/gallery.css'),
        ])
        self.pic_num = 0

    def process(self):
        BasePage.process(self)

        # get piece
        self.id = id = self.form.get('id', '')
        if id:
            try:
                self.piece = Piece(id)
            except DataRecordNotFound as e:
                self.piece_not_found = 1
        # get pic_num
        self.pic_num = int(self.form.get('pic_num', 0))

    def getPageContent(self):
        if self.piece_not_found:
            return p(f'Piece "{self.id}" not found.')
        if not self.piece:
            return p('No art piece selected.  Use piece_id=nn')

        return div(
            # self.formFields() + \
            self.getMainPic() + \
            self.getPicMenu() + \
            self.getPieceDescription(),
            id='pic-container')

    # def formFields(self):
    #     pic_id = input(name='id', value=self.id, type='hidden')
    #     pic_num = input(name='pic_num', value=self.pic_num, type='hidden')
    #     return pic_id + pic_num
            
    def getPicMenu(self):
        lis = ''
        if len(self.piece.images.tiny_urls) > 1:
            for i, image_url in enumerate(self.piece.images.tiny_urls):
                class_ = 'pic-menu-item'
                if i == self.pic_num:
                    class_ += ' pic-menu-selected'
                pic = img(src=f'{image_url}', id=f'pic-num-{i}',
                          class_=class_)
                lis += li(pic)
        return div(ul(lis, class_='piece-menu__list'), class_='piece-menu')

    def getMainPic(self):
        o = ''
        for i, url in enumerate(self.piece.images.display_urls):
            class_ = 'main-pic'
            if i == 0:
                class_ += ' selected'
            o += img(src=url, class_=class_)
        return div(o, id='main-pic-container')

    def getPieceDescription(self):
        template = self.getTemplate('piece_description.html')
        data = self.piece.data
        data.shows_info = self.getShowsInfo()
        return template.format(**data)

    def getShowsInfo(self):
        html = ''
        template = self.getTemplate('show_item.html')
        for show in self.piece.shows:
            data = {'name': show.name,
                    'gallery': show.contact.company_name,
                    'website': show.contact.website,
                    'city': show.contact.city,
                    'state': show.contact.state,
                    'start_date': show.start_date,
                    'end_date': show.end_date}
            html += template.format(**data)
        if html:
            html = '<p>In Shows:</p>' + html
        return html

if __name__ == '__main__':
    PiecePage().go()
