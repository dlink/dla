
from gallery import GalleryPage

class AvailableGalleryPage(GalleryPage):

    def __init__(self, id):
        GalleryPage.__init__(self, id)

    def getPieces(self):
        pieces_list = []
        for piece in super().getPieces():
            if 'Available' not in piece.status:
                continue
            pieces_list.append(piece)
        return pieces_list
    
if __name__ == '__main__':
    HomePage().go()
