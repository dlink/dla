from vlib import conf
from vlib.utils import lazyproperty
from vweb.html import a, img

class Thumbnail():

    def __init__(self, piece):
        self.piece = piece
        self.conf = conf.getInstance()

    @lazyproperty
    def html(self):
        template = self.getTemplate('thumbnail.html')
        piece = self.piece
        image_url = ''
        image_url = piece.images.thumb_urls[0]
        image_tag = img(src=f'/{image_url}')
        href=f'/piece/{piece.code}'
        image_link = a(image_tag, href=href)
        return template.format(
            image=image_link,
            name=piece.name,
            year=piece.created_year,
            materials=piece.material,
            dimensions=piece.dimensions,
            status='')
    
    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/templates/{filename}'
        return open(filepath, 'r').read()
