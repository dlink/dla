
from vweb.html import a, div, h2, li, ul

from basepage import BasePage
from shows import Shows

class ShowsPage(BasePage):

    def __init__(self):
        self.title = 'David Link Shows'
        BasePage.__init__(self, self.title)
        self.style_sheets.extend([
            self.versionize('css/shows.css'),
        ])        
        self.shows = Shows()

    def process(self):
        BasePage.process(self)

    def getPageContent(self):

        o = ''
        o += h2('Shows')
        items = ''
        for show in self.shows.getAll():
            items += li(self.getShowInfo(show))
        o += ul(items)
        return o

    def getShowInfo(self, show):
        href = f'/show/{show.code}'
        company_name = show.contact.company_name if show.contact else ''
        return \
            f"{show.year} {a(show.name, href=href)}, {show.location} - " \
            f"{company_name}"
            
