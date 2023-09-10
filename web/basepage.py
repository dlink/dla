import os

from vlib import conf

from vweb.htmlpage import HtmlPage

from header import Header

class BasePage(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPage() method
    '''

    def __init__(self, report_name=None):
        HtmlPage.__init__(self, report_name or 'Base Report')
        self.header = Header(self)
        self.conf = conf.getInstance()

        self.style_sheets.extend([
            self.versionize('css/basepage.css'),
        ])

    def versionize(self, file):
        timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir, file))
        return '%s?v=%s' % (file, timestamp)

    def getHtmlContent(self):
        template = self.getTemplate('basepage.html')
        data = {'header': self.header.getHeader(),
                'main': self.getPageContent()}
        return template.format(**data)

    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/templates/{filename}'
        return open(filepath, 'r').read()
