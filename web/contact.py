
from basepage import BasePage

class ContactPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link Contact Page')

    def getPageContent(self):
        return '<h3 style="margin: 20px">Contact Page</h2>'
