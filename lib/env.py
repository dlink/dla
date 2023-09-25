class Env():
    def __init__(self):
        self.verbose = 0

class EnvFactory():

    def __init__(self):
        self.instance = None

    def create(self):
        if not self.instance:
            self.instance = Env()
        return self.instance

envFactory = EnvFactory()

def getInstance():
    return envFactory.create()
