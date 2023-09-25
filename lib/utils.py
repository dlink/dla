import os

def mkdir_p(dirname):
    if os.path.exists(dirname):
        return 0
    os.mkdir(dirname)
    return 1
