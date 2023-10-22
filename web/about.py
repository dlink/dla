
from basepage import BasePage

class AboutPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link About Page')
        self.style_sheets.extend([
            self.versionize('css/about.css'),
        ])

    def getPageContent(self):
        return self.getTemplate('about.html')
