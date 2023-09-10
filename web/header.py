
class Header():

    def __init__(self, basePage):
        self.basePage = basePage

    def getHeader(self):
        template = self.basePage.getTemplate('header.html')
        return template
