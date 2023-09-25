#!/bin/env python

import os
from PIL import Image as Pil

from vlib.utils import lazyproperty, validate_num_args

class ImageError(Exception): pass

class Image():

    def __init__(self, filepath):
        self.filepath = filepath
        self.dir, self.filename, self.filename_wo, self.ext = \
            self.fileparts
        self.action_statuses = []

    def resize(self, width=None, height=None):
        if not width and not height:
            raise ImageError('resize: must specify either width or height.')

        img = Pil.open(self.filepath)
        old_width, old_height = img.size
        if width and not height:
            width = int(width)
            ratio = float(width / old_width)
            height = int(old_height * ratio)
        elif height and not width:
            height = int(height)
            ratio = float(height / old_height)
            width = int(old_width * ratio)
        else:
            width = int(width)
            height = int(height)
        resized_img = img.resize((width, height))

        # make backup of file
        done = bk = 0
        while not done:
            bk += 1
            dir = self.dir + '/' if self.dir else ''
            bk_filepath = f'{self.dir}{self.filename_wo}_bk{bk}{self.ext}'
            if not os.path.exists(bk_filepath):
                done = 1
        img.save(bk_filepath)

        # write file
        resized_img.save(self.filepath)

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
    def file_size(self):
        if os.path.exists(self.filepath):
            file_size_bytes = os.path.getsize(self.filepath)
            file_size_kb = file_size_bytes // 1024  # Convert to kilobytes
            #file_size_mb = file_size_kb // 1024     # Convert to megabytes
            return file_size_kb
        else:
            print("File does not exist.")

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
        return \
            f'{self.filepath}: {self.file_size}kb, {im.size}, '\
            f'{im.format}, {im.mode}'

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
        commands = [
            'resize <filepath> <width> <height>',
            'resize_by_width <filepath> <width>',
            'resize_by_height <filepath> <height>',
            'stat <filepath>',
            'to_png <filepath>',
        ]
        self.cli = CLI(self.process, commands)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
        '''
        args = list(args)
        cmd = args.pop(0)

        if cmd == 'resize':
            validate_num_args('resize', 3, args)
            filepath = args.pop(0)
            width = args.pop(0)
            height = args.pop(0)
            return Image(filepath).resize(width, height)
        if cmd in ('resize_by_width', 'resize_by_height'):
            validate_num_args('resize', 2, args)
            filepath = args.pop(0)
            pixels = args.pop(0)
            if 'width' in cmd:
                return Image(filepath).resize(width=pixels)
            else:
                return Image(filepath).resize(height=pixels)

        elif cmd == 'stat':
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
