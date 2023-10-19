
from basepage import BasePage

class HomePage(BasePage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self):
       BasePage.__init__(self, 'David Link Art')
       self.style_sheets.extend([
           self.versionize('css/home.css'),
       ])
       self.javascript_src.extend([
           self.versionize('js/home.js')
       ])

    def getPageContent(self):
        template = self.getTemplate('home.html')
        return template.format()
