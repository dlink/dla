
from vweb.html import div, hr, p

from basepage import BasePage
from shows_page import ShowsPage
from collections_page import CollectionsPage

class AboutPage(BasePage):

    def __init__(self):
        self.title = 'About Page | David Link Art'
        BasePage.__init__(self, self.title)
        self.style_sheets.extend([
            self.versionize('css/about.css'),
            self.versionize('css/collections.css'),
            self.versionize('css/shows.css'),
        ])

    def getPageContent(self):
        o = self.getTemplate('about.html')
        show_info = div(ShowsPage().getPageContent(), class_='left-side')
        collection_info = div(CollectionsPage().getPageContent(),
                              class_='right-side')
        o += div(
            collection_info + \
            hr(class_='divider') + \
            show_info,
            class_='container')
        return o
