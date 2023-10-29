
from vweb.html import a, div, h1, li, ul

from basepage import BasePage
from transactions import Transactions
from pieces import Piece

class CollectionsPage(BasePage):

    def __init__(self):
        self.title = 'David Link in Private Collections'
        BasePage.__init__(self, self.title)
        self.style_sheets.extend([
            self.versionize('css/collections.css'),
        ])
        self.transactions = Transactions()

    def process(self):
        BasePage.process(self)

    def getPageContent(self):

        o = ''
        o += h1('Private Collections')
        items = ''
        for transaction in self.transactions.getAll():
            items += li(self.getCollectionInfo(transaction))
        o += ul(items)
        return o

    def getCollectionInfo(self, transaction):
        owner = transaction.owner
        piece = Piece(transaction.piece_id)
        href = f'/piece/{piece.code}-{piece.version}'
        piece_name = f'{piece.name}-{piece.version}'
        piece_link = a(piece_name, href=href)

        if owner.authorized:
            owner_name = owner.name
        else:
            owner_name = 'Private'
        info = f'{owner_name}, {owner.city}, {owner.state} - {piece_link}'
        return info
