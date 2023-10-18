import os

from vlib import conf

from vweb.htmlpage import HtmlPage


class HeroTest(HtmlPage):
    '''Base Page for all pages on this site

       Subclass this class and provide the getPageContent() method
    '''

    def __init__(self):
       HtmlPage.__init__(self, 'Hero Test')
       self.conf = conf.getInstance()
       self.style_sheets.extend([
           self.versionize('css/hero_test.css'),
       ])
       self.javascript_src.extend([
           self.versionize('js/hero_test.js')
       ])


    def getHtmlContent(self):
        template = self.getTemplate('hero_test.html')
        return template.format()

    def getTemplate(self, filename):
        filepath = f'{self.conf.base_dir}/web/templates/{filename}'
        return open(filepath, 'r').read()

    def versionize(self, file):
        timestamp=os.path.getmtime('%s/web/%s' % (self.conf.base_dir, file))
        return '/%s?v=%s' % (file, timestamp)
