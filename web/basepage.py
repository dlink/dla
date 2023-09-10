
from vweb.htmlpage import HtmlPage

class BasePage(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPage() method
    '''
    
    def __init__(self, report_name=None):
        HtmlPage.__init__(self, report_name or 'Base Report')

#     def versionize(self, file):
#         timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir,file))
#         return '%s?v=%s' % (file, timestamp)

    def getHtmlContent(self):
        return self.getPage()
