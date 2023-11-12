from vweb.html import div, img, p

from basepage import BasePage

class PageNotFoundPage(BasePage):

    def __init__(self):
        self.title = 'David Link 404 Page'
        BasePage.__init__(self, self.title)
        self.style_sheets.extend([
             self.versionize('css/page_not_found.css'),
        ])

    def getPageContent(self):
        template = self.getTemplate('page_not_found.html')
        return template.format()

if __name__ == '__main__':
    PageNotFoundPage().go()
