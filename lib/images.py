#!/bin/env python

import os
from PIL import Image as Pil

from vlib.utils import lazyproperty, validate_num_args

import env

class Images():
    HIRES = 1200
    SIZES = {'tiny': 50,
             'thumb': 200,
             'display': 500,
             }

class ImageError(Exception): pass

class Image():

    def __init__(self, filepath):
        self.filepath = filepath
        self.dir, self.filename, self.filename_wo, self.ext = \
            self.fileparts
        self.action_statuses = []
        self.env = env.getInstance()
        self.verbose = self.env.verbose

    @lazyproperty
    def img(self):
        return Pil.open(self.filepath)

    def resize(self, width=None, height=None, outputfile=None, inplace=False):
        if not width and not height:
            raise ImageError('resize: must specify either width or height.')
        if not inplace and not outputfile:
            raise ImageError('Must specify outputfile or pass inplace=True')

        old_width, old_height = self.img.size
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
        resized_img = self.img.resize((width, height))

        if inplace:
            self.makeBackup()
            outputfile = self.filepath

        # write file
        resized_img.save(outputfile)

    def resize_pad(self, width, outputfile=None, inplace=False):
        '''Resize an image to to have a 4:3 aspect ratio with given width
           Pad image with white space if necessary.
        '''
        if not inplace and not outputfile:
            raise ImageError('Must specify outputfile or pass inplace=True')

        taspect_ratio = 4 /3

        width = input_width = int(width)
        height = calc_height = int(width * taspect_ratio)

        padded_img = Pil.new('RGB', (width, height), 'white')

        owidth, oheight = self.img.size
        oaspect_ratio = oheight / owidth
        if oaspect_ratio > taspect_ratio:
            width = int(height / oaspect_ratio)
        else:
            height = int(width * oaspect_ratio)
        resized_img = self.img.resize((width, height),
                                      Pil.Resampling.LANCZOS)
        paste_pos = ((padded_img.width - resized_img.width) // 2,
                     (padded_img.height - resized_img.height) // 2)
        padded_img.paste(resized_img, paste_pos)

        if self.verbose:
            print('input width:', input_width)
            print('calc height:', calc_height)
            print('orig width, height:', owidth, oheight)
            print('taspect_ratio:', round(taspect_ratio, 4))
            print('oaspect_ratio:', round(oaspect_ratio, 4))
            if width != input_width:
                print('changed width:', width)
            else:
                 print('changed height:', height)
            print('new width, height:', width, height)
            print('final width, height:', padded_img.width, padded_img.height)
            print('paste pos:', paste_pos)

        if inplace:
            self.makeBackup()
            outputfile = self.filepath

        # write file
        padded_img.save(outputfile)

    def rotate(self, outputfile=None, inplace=False):
        if not inplace and not outputfile:
            raise ImageError('Must specify outputfile or pass inplace=True')

        rotated_img = self.img.rotate(-90, expand=True)
        if inplace:
            self.makeBackup()
            outputfile = self.filepath
        rotated_img.save(outputfile)

    def makeBackup(self):
        done = bk = 0
        while not done:
            bk += 1
            dir = self.dir + '/' if self.dir else ''
            bk_filepath = f'{self.dir}{self.filename_wo}_bk{bk}{self.ext}'
            if not os.path.exists(bk_filepath):
                done = 1
        self.img.save(bk_filepath)

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

    @property
    def stat(self):
        #im = Pil.open(self.filepath)
        dpi_str = ''
        if 'dpi' in self.img.info:
            dpi = list(self.img.info['dpi'])
            dpi_str = f'({dpi[0]:.0f},{dpi[1]:.0f}) dpi'
        return \
            f'{self.filepath}: {self.file_size}kb, {self.img.size}, '\
            f'{dpi_str}, ' \
            f'{self.img.format}, {self.img.mode}'
    @property
    def size(self):
        return self.img.size
    @property
    def width(self):
        return self.img.size[0]
    @property
    def height(self):
        return self.img.size[1]

class ImagesCLIError(Exception): pass

class ImagesCLI(object):
    '''Command line interface to the Product Class
       Used for discovery
    '''

    def __init__(self):
        self.env = env.getInstance()

    def run(self):
        '''Set up Command Line (CLI) commands and options
           for Images Module
        '''
        from cli import CLI
        commands = [
            'resize <filepath> <width> <height> [<output_file>]',
            'resize_by_width <filepath> <width> [<output_file>]',
            'resize_by_height <filepath> <height> [<output_file>]',
            'resize_pad <filepath> <width> [<output_file>] # 4:3',
            'rotate <filepath> [<output_file>] # clockwise',
            'stat <filepath>',
            'to_png <filepath>',
        ]
        options = {'i': 'edit inplace'}
        self.cli = CLI(self.process, commands, options)
        self.cli.process()

    def process(self, *args):
        '''Process all Incoming Requests
        '''
        args = list(args)
        cmd = args.pop(0)

        if self.cli.hasoption.get('v'):
            self.env.verbose = 1

        if cmd == 'resize':
            num_args = 3
            if self.cli.hasoption.get('i'):
                num_args = 2
            validate_num_args('resize', num_args, args)
            filepath = args.pop(0)
            width = args.pop(0)
            height = args.pop(0)
            if self.cli.hasoption.get('i'):
                outputfile = None
                inplace = 1
            else:
                outputfile = args.pop(0)
                inplace = 0
            return Image(filepath).resize(width, height, outputfile, inplace)

        if cmd in ('resize_by_width', 'resize_by_height'):
            num_args = 2
            if self.cli.hasoption.get('i'):
                num_args = 1
            validate_num_args('resize', num_args, args)
            filepath = args.pop(0)
            pixels = args.pop(0)
            if self.cli.hasoption.get('i'):
                outputfile = None
                inplace = 1
            else:
                outputfile = args.pop(0)
                inplace = 0
            if 'width' in cmd:
                return Image(filepath).resize(
                    width=pixels, outputfile=outputfile, inplace=inplace)
            else:
                return Image(filepath).resize(
                    height=pixels, outputfile=outputfile, inplace=inplace)

        if cmd == 'resize_pad':
            num_args = 2
            if self.cli.hasoption.get('i'):
                num_args = 1
            validate_num_args('resize_pad', num_args, args)
            filepath = args.pop(0)
            width = args.pop(0)
            if self.cli.hasoption.get('i'):
                outputfile = None
                inplace = 1
            else:
                outputfile = args.pop(0)
                inplace = 0
            return Image(filepath).resize_pad(width, outputfile=outputfile,
                                              inplace=inplace)

        elif cmd == 'rotate':
            validate_num_args('rotate', 1, args)
            filepath = args.pop(0)
            if self.cli.hasoption.get('i'):
                outputfile = None
                inplace = 1
            else:
                outputfile = args.pop(0)
                inplace = 0
            return Image(filepath).rotate(outputfile, inplace=inplace)

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
