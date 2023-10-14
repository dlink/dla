import os

from vlib import conf

from vweb.htmlpage import HtmlPage

from header import Header
from nav import Nav
from aside import Aside

class BasePage(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self, report_name=None):
        HtmlPage.__init__(self, report_name or 'Base Report')
        self.conf = conf.getInstance()

        self.header = Header(self)
        self.nav = Nav(self)
        self.aside = Aside(self)

        self.style_sheets.extend([
            self.versionize('css/basepage.css'),
            self.versionize('css/header.css'),
            self.versionize('css/nav.css'),
            self.versionize('css/aside.css'),
            self.versionize('css/main.css'),
        ])

    def getHtmlContent(self):
        template = self.getTemplate('basepage.html')
        data = {'header': self.header.getHeader(),
                'nav': self.nav.getNav(),
                'aside': self.aside.getAside(),
                'main': self.getPageContent(),
                }
        return template.format(**data)

    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/templates/{filename}'
        return open(filepath, 'r').read()

    def versionize(self, file):
        timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir, file))
        return '/%s?v=%s' % (file, timestamp)
