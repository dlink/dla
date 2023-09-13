import os

from vlib import conf

from basepage import BasePage
from admin.header import Header
from admin.nav import Nav
from admin.aside import Aside

class AdminBasePage(BasePage):
    '''Base Page for all Admin pages on this site
       This class subclasses .BasePage

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self, report_name=None):
        BasePage.__init__(self, report_name or 'Admin Base Report')
        self.conf = conf.getInstance()

        self.header = Header(self)
        self.nav = Nav(self)
        self.aside = Aside(self)

        # self.style_sheets.extend([
        #     self.versionize('admin/css/basepage.css'),
        #     self.versionize('admin/css/nav.css'),
        # ])

    def getHtmlContent(self):
        template = super().getTemplate('basepage.html')
        data = {'header': self.header.getHeader(),
                'nav': self.nav.getNav(),
                'aside': self.aside.getAside(),
                'main': self.getPageContent(),
                }
        return template.format(**data)
    
    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/admin/templates/{filename}'
        return open(filepath, 'r').read()

