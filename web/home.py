
from basepage import BasePage

class HomePage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'DLA')

    def getPage(self):
        return '<p>Home Page</p>'
    
if __name__ == '__main__':
    HomePage().go()


