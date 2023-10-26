
from vlib.datarecord import DataRecordNotFound

from vlib.utils import format_date, is_int
from vweb.html import a, div, li, p, ul

from basepage import BasePage
from shows import Show
from pieces import Piece
from thumbnails import Thumbnail

class ShowPage(BasePage):

    def __init__(self, id):
        title = 'David Link '
        if is_int(id):
            title += f'Show {id}'
        else:
            title += f'Show: {id.title()}'
        BasePage.__init__(self, title)
        self.id = id
        self.show = None
        self.show_not_found = 0
        self.style_sheets.extend([
             self.versionize('css/show.css'),
             self.versionize('css/gallery.css'),
             self.versionize('css/thumbnails.css'),
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
        return div(p(a('All Shows', href='/shows')), class_='show-header')

    def getShowsInfo(self):
        html = ''
        template = self.getTemplate('show_item.html')
        if self.show.contact:
            company_name = self.show.contact.company_name
            website = self.contact.website or ''
            city = self.contact.city or ''
            state = self.contact.city or ''
        else:
            company_name = website = city = state = ''

        data = {'show_code': self.show.code,
                'name': self.show.name,
                'gallery': company_name,
                'website': website,
                'city': city,
                'state': state,
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
