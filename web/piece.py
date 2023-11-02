from flask import request

from vlib.datarecord import DataRecordNotFound
from vlib.utils import is_int, format_date

from vweb.htmltable import HtmlTable
from vweb.html import a, div, h1, img, input, li, p, span, ul

from basepage import BasePage
from pieces import Piece
from thumbnails import Thumbnail

class PiecePage(BasePage):

    def __init__(self, id):
        self.title = 'David Link '
        if is_int(id):
            self.title += f'Piece {id}'
        else:
            self.title += id.title().replace('_', ' ')
        BasePage.__init__(self, self.title)
        self.id = id
        self.piece = None
        self.piece_not_found = 0
        self.javascript_src.extend(['/js/piece.js'])
        self.style_sheets.extend([
            self.versionize('css/piece.css'),
            self.versionize('css/gallery.css'),
            self.versionize('css/thumbnails.css'),
        ])
        self.pic_num = 0
        try:
            self.piece = Piece(self.id)
        except DataRecordNotFound as e:
            self.piece_not_found = 1

    def process(self):
        BasePage.process(self)

        # get pic_num
        self.pic_num = int(self.form.get('pic_num', 0))

    def getPageContent(self):
        if self.piece_not_found:
            return div(p(f'Piece "{self.id}" not found.'),
                       class_='error-msg')

        output = \
            h1(self.piece.name) + \
            self.getBreadCrumbs() + \
            self.getMainPic() + \
            self.getPicMenu() + \
            self.getPieceInfo() + \
            self.getVersions() + \
            self.getPieceDescription()

        return div(output, id='main-container')

    def getBreadCrumbs(self):
        referrer = request.referrer
        if '/gallery' in str(referrer):
            href = referrer[referrer.find('/gallery'):]
            return p(a('< back', href=href), # ◀
                     class_='bread-crumbs')
        return ''

    def getPicMenu(self):
        lis = ''
        if len(self.piece.images.tiny_urls) > 1:
            for i, image_url in enumerate(self.piece.images.tiny_urls):
                class_ = 'pic-menu-item'
                if i == self.pic_num:
                    class_ += ' pic-menu-selected'
                pic = img(src=f'/{image_url}', id=f'pic-num-{i}',
                          class_=class_)
                lis += li(pic)
        return div(ul(lis, class_='piece-menu__list'), class_='piece-menu')

    def getMainPic(self):
        o = ''
        for i, url in enumerate(self.piece.images.display_urls):
            orig_url = f'/{self.piece.images.orig_urls[i]}'
            class_ = 'main-pic'
            if i == 0:
                class_ += ' selected'
            o += a(img(src=f'/{url}', class_=class_), href=orig_url)
        return div(o, id='main-pic-container')

    def getVersions(self):
        lis = ''
        for v in self.piece.versions:
            lis += li(Thumbnail(v).html)
        if lis:
            gallery = div(ul(lis, class_='gallery__list small'),
                          class_='gallery')
            return div(p('Other Versions:') +
                       gallery,
                       id='other-versions')
        return ''

    def getPieceInfo(self):
        template = self.getTemplate('piece_info.html')
        data = self.piece.data
        data.status_info = self.piece.status_info
        return template.format(**data)

    def getPieceDescription(self):
        template = self.getTemplate('piece_description.html')
        data = self.piece.data
        data.short_description = data.short_description or ''
        data.shows_info = self.getShowsInfo()
        return template.format(**data)

    def getShowsInfo(self):
        html = ''
        template = self.getTemplate('show_item.html')

        for show in self.piece.shows:
            if show.start_date:
                start_date = format_date(show.start_date)
                end_date = format_date(show.end_date)
                dates = f'{start_date} - {end_date}'
            else:
                dates = show.year
            data = {'show_code': show.code,
                    'name': show.name,
                    'gallery': show.contact.company_name,
                    'website': show.contact.website,
                    'city': show.contact.city,
                    'state': show.contact.state,
                    'dates': dates}
            html += template.format(**data)
        if html:
            html = '<p>In Shows:</p>' + html
        return html
