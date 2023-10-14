
from vlib.datarecord import DataRecordNotFound

#from vweb.htmltable import HtmlTable
#from vweb.html import div, img, input, li, p, span, ul
from vlib.utils import format_date
from vweb.html import div, li, p, ul

from basepage import BasePage
from shows import Show
#from thumbnails import Thumbnail

class ShowPage(BasePage):

    def __init__(self, id):
        BasePage.__init__(self, 'Show Page')
        self.id = id
        self.show = None
        self.show_not_found = 0
        self.style_sheets.extend([
             self.versionize('css/main.css'),
             self.versionize('css/show.css'),
             self.versionize('css/gallery.css'),
         ])

    def process(self):
        BasePage.process(self)

        # get piece
        try:
            self.show = Show(self.id)
        except DataRecordNotFound as e:
            self.show_not_found = 1

    def getPageContent(self):
        if self.show_not_found:
            return p(f'Show "{self.id}" not found.')
        if not self.show:
            return p('No art show selected.  Use show_id=nn')

        template = self.getTemplate('show_item.html')
        
        return div(
            self.getHeader() + 
            self.getShowsInfo() +
            self.getDescription() +
            self.getPieces(),
            id='main-container')

    def getHeader(self):
        return div(p('Art Show'), class_='show-header')

    def getShowsInfo(self):
        html = ''
        template = self.getTemplate('show_item.html')
        data = {'show_code': self.show.code,
                'name': self.show.name,
                'gallery': self.show.contact.company_name,
                'website': self.show.contact.website,
                'city': self.show.contact.city,
                'state': self.show.contact.state,
                'start_date': format_date(self.show.start_date),
                'end_date': format_date(self.show.end_date)}
        html += template.format(**data)
        return html

    def getDescription(self):
        return div(
            text2html(self.show.description),
            class_='show-description'
        )

    def getPieces(self):
        from pieces import Piece
        from thumbnails import Thumbnail
        
        pieces = []
        for piece_id in self.show.piece_ids:
            pieces.append(Piece(piece_id))

        #pieces_html = '<br>'.join([p.name for p in pieces])
        lis = ''
        for piece in pieces:
            lis += li(Thumbnail(piece).html)
        pieces_html =  div(ul(lis, class_='gallery__list'), class_='gallery')
        
        return div(
            div('Pieces:', class_='pieces-header') +
            pieces_html,
            class_='show-pieces'
        )
    
def text2html(text):
    if not text:
        return ''
    return text.replace('\n', '<br/>')

if __name__ == '__main__':
    ShowPage().go()
