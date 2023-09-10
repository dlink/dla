
class Footer():

    def __init__(self, basePage):
        self.basePage = basePage

    def getFooter(self):
        template = self.basePage.getTemplate('footer.html')
        return template
