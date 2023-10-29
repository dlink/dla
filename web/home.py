
from basepage import BasePage

class HomePage(BasePage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self):
        self.title = 'David Link Art'
        BasePage.__init__(self, self.title)
        self.style_sheets.extend([
            self.versionize('css/home.css'),
        ])
        self.javascript_src.extend([
            self.versionize('js/home.js')
        ])

    @property
    def meta_description(self):
        return \
            'David Link is an artists who creates bold, modern, and minimal ' \
            'geometric works of art'

    def getPageContent(self):
        template = self.getTemplate('home.html')
        return template.format()
