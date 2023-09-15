from vlib import conf
from vlib.utils import lazyproperty
from vweb.html import img

class Thumbnail():

    def __init__(self, piece):
        self.piece = piece
        self.conf = conf.getInstance()

    @lazyproperty
    def html(self):
        template = self.getTemplate('thumbnail.html')
        piece = self.piece 
        return template.format(
            image_url=piece.images.urls[0],
            name=piece.name,
            year=piece.created_year,
            materials=piece.material,
            dimensions=piece.dimensions,
            status='')
    
    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/templates/{filename}'
        return open(filepath, 'r').read()
