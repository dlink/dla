
from vlib import db
from vlib import conf
from vlib.datatable import DataTable
from vlib.odict import odict
from vlib.utils import lazyproperty

from utils import mkdir_p

class PieceImages():

    def __init__(self, piece):
        self.piece = piece
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        self.pieceImagesDt = DataTable(self.db, 'piece_images')
        self.image_basedir = \
            f'{self.conf.data_dir}/images/pieces/{self.piece.code}'
        self.url_basepath = f'images/pieces/{self.piece.code}'
        self.getImages()

    def initImageDirs(self):
        mkdir_p(f'{self.image_basedir}/display')
        mkdir_p(f'{self.image_basedir}/thumb')
        mkdir_p(f'{self.image_basedir}/tiny')

    def getImages(self):
        '''Return a list of piece_image odicts
           Read database records
           Add filepath, and url
        '''
        self.pieceImagesDt.setFilters({'piece_id': self.piece.id})
        self.data = []
        for pi in self.pieceImagesDt.getTable():
            pi = odict(pi)
            pi.filepath = f'{self.image_basedir}/{pi.filename}'

            pi.url = f'{self.url_basepath}/display/{pi.filename}'
            pi.tiny_url = f'{self.url_basepath}/tiny/{pi.filename}'
            pi.thumb_url = f'{self.url_basepath}/thumb/{pi.filename}'

            self.data.append(pi)

    @lazyproperty
    def filepaths(self):
        return [pi.filepath for pi in self.data]

    @lazyproperty
    def urls(self):
        return [pi.url for pi in self.data]
    @lazyproperty
    def tiny_urls(self):
        return [pi.tiny_url for pi in self.data]
    @lazyproperty
    def thumb_urls(self):
        return [pi.thumb_url for pi in self.data]

