
from vlib import db
from vlib import conf
from vlib.datatable import DataTable
from vlib.odict import odict
from vlib.utils import lazyproperty

class PieceImages():

    def __init__(self, piece):
        self.piece = piece
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        self.pieceImagesDt = DataTable(self.db, 'piece_images')
        self.loadImages()

    def loadImages(self):
        '''Return a list of piece_image odicts
           Read database records
           Add filepath, and url
        '''
        self.pieceImagesDt.setFilters({'piece_id': self.piece.id})
        image_dir = f'{self.conf.data_dir}/images/pieces/{self.piece.code}'
        url_basepath = f'images/pieces/{self.piece.code}'
        self.data = []
        for pi in self.pieceImagesDt.getTable():
            pi = odict(pi)
            pi.filepath = f'{image_dir}/{pi.filename}'
            pi.url = f'{url_basepath}/{pi.filename}'
            self.data.append(pi)
        
    @lazyproperty
    def filepaths(self):
        return [pi.filepath for pi in self.data]

    @lazyproperty
    def urls(self):
        return [pi.url for pi in self.data]

