import os
from flask import request

from vlib import conf
from vlib import logger

from vweb.htmlpage import HtmlPage

from aside import Aside

class BasePage(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self, title='David Link Art'):
        HtmlPage.__init__(self, title or 'Base Report')
        self.conf = conf.getInstance()
        self.logger = logger.getLogger(__class__.__name__)
        self.aside = Aside(self)
        self.style_sheets.extend([
            self.versionize('css/basepage.css'),
            self.versionize('css/header.css'),
            self.versionize('css/footer.css'),
        ])
        self.javascript_src.extend(['/js/header.js'])
        self.logPageLoad(title)
        self.metadata = {'description': self.meta_description}
        self.favicon_path = '/images/favicon/favicon.ico'
        self.ga_tag = self.getGATag()

    @property
    def meta_description(self):
        return \
            f'{self.title} - Bold, modern, and minimal geometric works of art'

    def logPageLoad(self, title):
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        self.logger.info(f'{user_ip}: {request.path}')

    def getHtmlContent(self):
        template = self.getTemplate('basepage.html')
        data = {'header': self.getTemplate('header.html'),
                'aside': self.aside.getAside(),
                'main': self.getPageContent(),
                'footer': self.getTemplate('footer.html'),
                }
        return template.format(**data)

    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/html/{filename}'
        return open(filepath, 'r').read()

    def versionize(self, file):
        timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir, file))
        return '/%s?v=%s' % (file, timestamp)

    def getGATag(self):
        if self.conf.system != 'prod':
            return ''

        return self.getTemplate('ga_tag.html')
