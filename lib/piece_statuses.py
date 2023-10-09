
from vlib import db
from vlib.attributes import Attributes

class PieceStatuses(Attributes):

    def __init__(self):
        self.db = db.getInstance()
        Attributes.__init__(self, self.db, 'piece_statuses', 'id')

def test():
    pieceStatuses = PieceStatuses()
    print(pieceStatuses.SOLD)

if __name__ == '__main__':
    test()
