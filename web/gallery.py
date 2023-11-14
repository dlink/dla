
from vweb.htmltable import HtmlTable
from vweb.html import div, h1, li, p, span, ul
from vlib.utils import is_int
from vlib.odict import odict

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
        self.javascript_src.extend([
            self.versionize('js/gallery.js')
        ])

    def process(self):
        super().process()
        self.not_found = 0
        self.medium = None
        try:
            self.medium = Medium(self.id)
        except:
            self.not_found = 1
        self.size_range = self.form.get('size_range')
        self.status = self.form.get('status')

    def getPageContent(self):
        if self.not_found:
            return self.notFound()

        return div(
            self.getPageHeader() + \
            self.getSearchForm() + \
            self.getThumbnails(), class_='gallery')

    def getPageHeader(self):
        o = ''
        o += h1(self.medium.name_plural)
        if self.medium.code == 'sculpture':
            o += span(f'{(self.status or "All").title()}',
                      class_='filter_desc')
            o += span(f'Size Range: {self.size_range or "All"}',
                      class_='filter_desc')
        return div(o, class_='header_container')

    def getThumbnails(self):
        pieces = self.pieces.get({'medium_id': self.medium.id},
                                 self.medium.sort_order)
        lis = ''
        for piece in pieces:
            # not in gallery
            if not piece.show_in_gallery:
                continue
            # status
            if self.status and self.status not in piece.status.lower():
                continue
            # size_range
            if self.size_range and piece.size_range != self.size_range:
                continue

            lis += li(Thumbnail(piece).html)

        if not lis:
            emsg = f'No pieces found for gallery "{self.id}".'
            if self.size_range:
                emsg += f' size_range: "{self.size_range}"'
            output = p(emsg)
        else:
            output = ul(lis, class_='gallery__list')
        return output

    def getSearchForm(self):
        if self.medium.code != 'sculpture':
            return ''

        data = odict(
            status = odict(
                all='',
                available=''),
            size_range = odict(
                all='',
                small='',
                medium='',
                large='',
            )
        )
        if self.status:
            data.status[self.status] = 'selected'
        if self.size_range:
            data.size_range[self.size_range] = 'selected'
        template = self.getTemplate('gallery_search.html')
        return template.format(**data)

    def notFound(self):
        return p(f'Gallery: "{self.id}" not found', class_='error-msg')

if __name__ == '__main__':
    HomePage().go()
