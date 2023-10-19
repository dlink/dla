
from basepage import BasePage

class AboutPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'About Page')
        self.style_sheets.extend([
             self.versionize('css/main.css'),
         ])

    def getPageContent(self):
        return '<h3 style="margin: 20px">About Page</h2>'
