
from vlib.odict import odict
from vweb.html import a, b, div, h2, i, li, p, span, ul

from basepage import BasePage
from transactions import Transactions
from pieces import Piece

TRANSTYPES = {
    'sale': 'Sales',
    'donation': 'Donations',
    'gift': 'Gifted',
    }

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

        # consolidate by transaction_type, owner
        data = {}
        for transaction in self.transactions.getAll():
            type = transaction.type
            owner = transaction.owner
            if type not in data:
                data[type] = {}
            if owner.id not in data[type]:
                data[type][owner.id] = odict(
                    {'transaction': transaction,
                     'owner': owner,
                     'pieces': []})
            piece = Piece(transaction.piece_id)
            data[type][owner.id].pieces.append(piece)

        # report
        for type, type_rec in data.items():
            if type != 'sale':
                o += p(b(TRANSTYPES[type]), class_='trans-type')

            for owner_id, owner_rec in type_rec.items():
                transaction = owner_rec.transaction
                owner = owner_rec.owner
                pieces = owner_rec.pieces
                o += p(self.getOwnerInfo(owner))
                items = ''
                for piece in pieces:
                    items += li(self.getPieceInfo(transaction, piece))
                o += ul(items)
        return o

    def getOwnerInfo(self, owner):
        if owner.authorized:
            owner_name = owner.name
        else:
            owner_name = 'Private'
        return f'{owner_name}, {owner.city}, {owner.state}'

    def getPieceInfo(self, transaction, piece):
        if piece.version > 1:
            href = f'/piece/{piece.code}-{piece.version}'
            piece_name = f'{piece.name}' + \
                span(f'-{piece.version}', class_='version')
        else:
            href = f'/piece/{piece.code}'
            piece_name = piece.name
        piece_link = a(piece_name, href=href)
        if piece.editions > 1:
            edition = span(f'(Edition {transaction.edition})',
                           class_='edition')
        else:
            edition = ''
        return f'{piece_link} {edition}'
