import os

def mkdir_p(dirname):
    if os.path.exists(dirname):
        return 0
    os.makedirs(dirname)
    return 1
