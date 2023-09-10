
from basepage import BasePage

class HomePage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'DLA')

    def getPageContent(self):
        template = self.getTemplate('home.html')
        return template

if __name__ == '__main__':
    HomePage().go()
