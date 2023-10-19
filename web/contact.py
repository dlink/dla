
from basepage import BasePage

class ContactPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link Contact Page')
        self.style_sheets.extend([
             self.versionize('css/main.css'),
         ])

    def getPageContent(self):
        return '<h3 style="margin: 20px">Contact Page</h2>'
