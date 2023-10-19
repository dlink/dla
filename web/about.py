
from basepage import BasePage

class AboutPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link About Page')

    def getPageContent(self):
        return '<h3 style="margin: 20px">About Page</h2>'
