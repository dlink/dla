#!/bin/env python

from PIL import Image as Pil

from vlib.utils import lazyproperty, validate_num_args

class Image():

    def __init__(self, filepath):
        self.filepath = filepath

    @lazyproperty
    def stat(self):
        im = Pil.open(self.filepath)
        Image(self.filepath)
        return f'{self.filepath}: {im.size}, {im.format}, {im.mode}'

class ImagesCLIError(Exception): pass

class ImagesCLI(object):
    '''Command line interface to the Product Class
       Used for discovery
    '''

    def run(self):
        '''Set up Command Line (CLI) commands and options
           for Images Module
        '''
        from cli import CLI
        commands = ['stat <filepath>']
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
        '''
        args = list(args)
        cmd = args.pop(0)

        if cmd == 'stat':
            validate_num_args('stat', 1, args)
            filepath = args.pop(0)
            return Image(filepath).stat
        else:
            raise ImagesCLIError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    ImagesCLI().run()
