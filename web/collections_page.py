
from vweb.html import a, b, div, h2, i, li, p, span, ul

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
        o += h2('Private Collections')

        # sales
        items = ''
        o += p(b('Sales'))
        for transaction in self.transactions.getAll():
            if transaction.type == 'sale':
                items += li(self.getCollectionInfo(transaction))
        o += ul(items)

        # donations
        items = ''
        o += p(b('Donations'))
        for transaction in self.transactions.getAll():
            if transaction.type == 'donation':
                items += li(self.getCollectionInfo(transaction))
        o += ul(items)

        # gifts
        items = ''
        o += p(b('Gifted'))
        for transaction in self.transactions.getAll():
            if transaction.type == 'gift':
                items += li(self.getCollectionInfo(transaction))
        o += ul(items)
        return o

    def getCollectionInfo(self, transaction):
        owner = transaction.owner
        piece = Piece(transaction.piece_id)
        href = f'/piece/{piece.code}-{piece.version}'
        if piece.version > 1:
            piece_name = f'{piece.name}-{piece.version}'
        else:
            piece_name = piece.name
        piece_link = a(piece_name, href=href)
        if piece.editions > 1:
            edition = span(f'(Edition {transaction.edition})',
                           class_='edition')
        else:
            edition = ''

        if owner.authorized:
            owner_name = owner.name
        else:
            owner_name = 'Private'
        info = \
            f'{owner_name}, {owner.city}, {owner.state}<br>{piece_link} ' \
            f'{edition}'
        return info
