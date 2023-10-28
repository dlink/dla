
from vweb.html import a, div, h1, li, ul

from basepage import BasePage
from sales import Sales

class CollectionsPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link in Private Collections')
        self.style_sheets.extend([
            self.versionize('css/collections.css'),
        ])
        self.sales = Sales()

    def process(self):
        BasePage.process(self)

    def getPageContent(self):

        o = ''
        o += h1('Private Collections')
        items = ''
        for sale in self.sales.getAll():
            items += li(self.getCollectionInfo(sale))
        o += ul(items)
        return o

    def getCollectionInfo(self, sale):
        owner = sale.owner
        piece = sale.piece
        href = f'/piece/{piece.code}-{piece.version}'
        piece_name = f'{piece.name}-{piece.version}'
        piece_link = a(piece_name, href=href)

        info = f'{owner.city}, {owner.state}, {piece_link}'
        if  owner.authorized:
            info = f'{owner.name} {info}'
        return info
