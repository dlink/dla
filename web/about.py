
from basepage import BasePage
from shows_page import ShowsPage

class AboutPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link About Page')
        self.style_sheets.extend([
            self.versionize('css/about.css'),
            self.versionize('css/shows.css'),
        ])

    def getPageContent(self):
        o = self.getTemplate('about.html')
        o += ShowsPage().getPageContent()
        return o
