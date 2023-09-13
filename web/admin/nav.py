
class Nav():

    def __init__(self, basePage):
        self.basePage = basePage

    def getNav(self):
        template = self.basePage.getTemplate('nav.html')
        return template
