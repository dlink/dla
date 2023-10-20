import os

from vlib import conf

from vweb.htmlpage import HtmlPage

from aside import Aside

class BasePage(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self, report_name=None):
        HtmlPage.__init__(self, report_name or 'Base Report')
        self.conf = conf.getInstance()
        self.aside = Aside(self)
        self.style_sheets.extend([
            self.versionize('css/basepage.css'),
            self.versionize('css/header.css'),
            self.versionize('css/footer.css'),
        ])
        self.javascript_src.extend(['/js/header.js'])

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
