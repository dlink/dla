#!/bin/env python

import os
from PIL import Image as Pil

from vlib.utils import lazyproperty, validate_num_args

class Image():

    def __init__(self, filepath):
        self.filepath = filepath
        self.dir, self.filename, self.filename_wo, self.ext = \
            self.fileparts
        self.action_statuses = []

    def to_png(self):
        '''Create a png file'''
        if self.ext == '.png':
            self.action_statuses.append(
                f'No action: file {self.filename} is already a png')
            return
        outfilepath = f'{self.dir}/{self.filename_wo}.png'
        im = Pil.open(self.filepath)
        im.save(outfilepath, 'PNG')
        im.close()
        self.action_statuses.append(f'{outfilepath} created.')

    @lazyproperty
    def fileparts(self):
        '''Return
              directory  : /data/dla/images/pieces/break_free
              filename   : Break_Free.png
              filename_wo: Break_Free
              extension  : .png
        '''
        directory, filename_with_extension = os.path.split(self.filepath)
        filename_wo, extension = os.path.splitext(filename_with_extension)
        filename = filename_wo + extension
        return directory, filename, filename_wo, extension

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
        commands = ['stat <filepath>',
                    'to_png <filepath>',
                    ]
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
        if cmd == 'to_png':
            validate_num_args('to_png', 1, args)
            filepath = args.pop(0)
            im = Image(filepath)
            im.to_png()
            print(im.action_statuses[-1])
        else:
            raise ImagesCLIError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    ImagesCLI().run()
