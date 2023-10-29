
from vweb.html import div, p

from basepage import BasePage
from shows_page import ShowsPage
from collections_page import CollectionsPage

class AboutPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link About Page')
        self.style_sheets.extend([
            self.versionize('css/about.css'),
            self.versionize('css/shows.css'),
        ])

    def getPageContent(self):
        o = self.getTemplate('about.html')
        show_info = div(ShowsPage().getPageContent(), class_='left-side')
        collection_info = div(CollectionsPage().getPageContent(),
                              class_='right-side')
        o += div(
            collection_info + \
            show_info,
            class_='container')
        return o
