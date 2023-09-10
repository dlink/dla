
class Aside():

    def __init__(self, basePage):
        self.basePage = basePage

    def getAside(self):
        template = self.basePage.getTemplate('aside.html')
        return template
