
from admin.basepage import AdminBasePage

class AdminPage(AdminBasePage):

    def __init__(self):
        AdminBasePage.__init__(self, 'David Link Admin')

    def getPageContent(self):
        template = self.getTemplate('admin.html')
        return template

if __name__ == '__main__':
    HomePage().go()
