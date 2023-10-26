
from vweb.html import a, div, h1, li, ul

from basepage import BasePage
from shows import Shows

class ShowsPage(BasePage):

    def __init__(self):
        BasePage.__init__(self, 'David Link Shows')
        self.style_sheets.extend([
            self.versionize('css/shows.css'),
        ])        
        self.shows = Shows()

    def process(self):
        BasePage.process(self)

    def getPageContent(self):

        o = ''
        o += h1('Shows')
        items = ''
        for show in self.shows.getAll():
            items += li(self.getShowInfo(show))
        o += ul(items)
        return o

    def getShowInfo(self, show):
        href = f'/show/{show.code}'
        company_name = show.contact.company_name if show.contact else ''
        return \
            f"{a(show.name, href=href)} - " \
            f"{show.start_date.year} {company_name}"
            
