
import os
import shutil

from vlib import db
from vlib import conf
from vlib.datatable import DataTable
from vlib.odict import odict
from vlib.utils import lazyproperty

from images import Images, Image
from utils import mkdir_p
import env

PAGE_COLOR = 'light_ivory'

class PieceImagesError(Exception): pass

class PieceImages():

    def __init__(self, piece):
        self.piece = piece
        self.db = db.getInstance()
        self.conf = conf.getInstance()
        self.pieceImagesDt = DataTable(self.db, 'piece_images')
        self.file_basedir = \
            f'{self.conf.data_dir}/images/pieces/{self.piece.code}'
        self.url_basepath = f'images/pieces/{self.piece.code}'
        if piece.edition > 1:
            self.file_basedir += f'/{piece.edition}'
            self.url_basepath += f'/{piece.edition}'
        self.getImages()
        self.warnings = []
        self.env = env.getInstance()
        self.verbose = self.env.verbose

    def initImageDirs(self):
        mkdir_p(self.file_basedir)
        mkdir_p(f'{self.file_basedir}/orig')
        mkdir_p(f'{self.file_basedir}/display')
        mkdir_p(f'{self.file_basedir}/thumb')
        mkdir_p(f'{self.file_basedir}/tiny')

    def addImage(self, img_filepath):
        img = Image(img_filepath)

        # copy image into directory structure
        self.initImageDirs()
        shutil.copy(img_filepath, f'{self.file_basedir}/orig/')
        if self.verbose:
            print(f'{self.file_basedir}/orig/{img.filename} added.')

        # create small images
        self.createSmallImages(img_filepath)

        # update database
        data = {'piece_id': self.piece.id,
                'filename': img.filename,
                'active': 1}
        self.pieceImagesDt.setFilters(data)
        if not self.pieceImagesDt.getTable():
            self.pieceImagesDt.insertRow(data)
            print(f'{img.filename} added.')

    def updateImages(self):
        for image in self.data:
            self.createSmallImages(image.filepath)

    def createSmallImages(self, img_filepath):
        self.warnings = []

        # instanciate Image Obj
        img = Image(img_filepath)

        # check stats on input - make sure it is high res
        if img.width < Images.HIRES or img.height < Images.HIRES:
            self.warnings.append(f'Image is not hi-res: {img.size}')

        # resize image for each size type:
        for size in Images.SIZES.keys():
            width = Images.SIZES[size]
            outputfile = f'{self.file_basedir}/{size}/{img.filename}'
            img.resize_pad(width=width, outputfile=outputfile,
                           color=PAGE_COLOR)
            if self.verbose:
                print(f'{outputfile} created')

        self.printWarnings()

    def getImages(self):
        '''Return a list of piece_image odicts
           Read database records
           Add filepath, and url
        '''
        self.pieceImagesDt.setFilters({'piece_id': self.piece.id})
        self.pieceImagesDt.setOrderBy('sort_order')
        self.data = []
        for pi in self.pieceImagesDt.getTable():
            pi = odict(pi)
            pi.filepath = f'{self.file_basedir}/orig/{pi.filename}'
            pi.url = f'{self.url_basepath}/display/{pi.filename}'
            pi.tiny_url = f'{self.url_basepath}/tiny/{pi.filename}'
            pi.thumb_url = f'{self.url_basepath}/thumb/{pi.filename}'
            self.data.append(pi)

        if not self.data:
            pi = odict()
            url_basepath = 'images/pieces/missing_image'
            pi.url = f'{url_basepath}/display/missing_image.png'
            pi.tiny_url = f'{url_basepath}/tiny/missing_image.png'
            pi.thumb_url = f'{url_basepath}/thumb/missing_image.png'
            self.data.append(pi)

    def printWarnings(self):
        for warning in self.warnings:
            print(f'WARNING: {warning}')

    @property
    def filepaths(self):
        return [pi.filepath for pi in self.data]

    @property
    def display_urls(self):
        return [pi.url for pi in self.data]
    @property
    def thumb_urls(self):
        return [pi.thumb_url for pi in self.data]
    @property
    def tiny_urls(self):
        return [pi.tiny_url for pi in self.data]

