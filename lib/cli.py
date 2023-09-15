#!/bin/env python

# Command Line Interface

import sys
import os
from copy import copy

#from pprint import pprint

class CLI_Error(Exception): pass

class CLI(object):
    '''Command Line Interface

       Usage:
          from cli import CLI, CLI_Error

          class MyClass(object):
             def run(self):
                 commands = [<list of commands>]
                 # Optional options
                 # options = {'a': 'human readable'}
                 self.cli = CLI(self.process, commands, [<options_dict>])
                 print(self.cli.process())

            def process(self, *args):
                # Do something with args
                args = list(args)
                cmd = args.pop(0)

                if cmd == 'mud':
                    return 'great'
                else:
                    raise CLI_Error('Unrecognized command: %s' % cmd)

       See Test Class for example
    '''
    def __init__(self, process_method, commands, options={}):
        self.process_method = process_method
        self.commands = commands
        self.options = options
        self.hasoption = {}
        if 'e+' not in self.options:
            self.options['e+'] = 'Email To <email1>[,<email2>[,...]]'
        if 'h' not in self.options:
            self.options['h'] = 'HTML output'
        if 'p' not in self.options:
            self.options['p'] = 'pprint'
        if 'q' not in self.options:
            self.options['q'] = 'Quite'
        if 'v' not in self.options:
            self.options['v'] = 'Verbose'

        self.verbose = False
        self.evocation_args = None

    def process(self):
        '''Process Command Line Arguments
           
           call process_method(**args)

           sets self.verbose
           
           Exists with status
                0 - success
                1 - syntax displayed and not action taken
              100 - fail
        '''

        args = copy(sys.argv[1:])
        self.evocation_args = copy(args)

        # options
        #   set things like self.hasoption['v'], etc

        for opt in self.options:

            # option takes argument?
            takes_value = 0
            if opt[-1] == '+':
                takes_value = 1
                opt = opt[0:-1]
                
            cmdopt = '-' + opt
            if cmdopt in args:
                p = args.index(cmdopt)

                # options that take arguments. eq. -e <email_recipients>
                if takes_value:
                    if len(args) < p+2:
                        raise Exception('-%s option requires a value' % opt)
                    value = args[p+1]
                    self.hasoption[opt] = value
                    args = args[0:p]+args[p+2:]

                # options that do not take arguments.  eq. -v
                else:
                    self.hasoption[opt] = True
                    args = args[0:p]+args[p+1:]
            else:
                self.hasoption[opt] = False

        if not args:
            self.syntax()

        retcode = 0
        try:
            results = self.process_method(*args)
        except Exception as e:
            if self.hasoption.get('v'):
                raise
            results = "Error: %s: %s" % (e.__class__.__name__, str(e))
            retcode = 100

        if self.hasoption.get('e'):
            self.emailResults(results, self.hasoption.get('e'))

        elif not self.hasoption.get('q'):
            if self.hasoption.get('h'):
                print_pretty(results, html=True)
            else:
                print_pretty(results, use_pprint=self.hasoption.get('p'))
                #pprint(results)

        sys.exit(retcode)

    def syntax(self, emsg=None):
        prog = os.path.basename(sys.argv[0])
        if emsg:
            print(emsg)
        ws = ' '*len(prog)

        options = '[OPTIONS]'

        print()
        for i, command in enumerate(self.commands):
            a = prog if i == 0 else ' '*len(prog)
            b = options if i == 0 else ' '*len(options)
            print(' %s %s %s' % (a, b, command))
        print()
        for o, desc in list(self.options.items()):
            o2 = o.replace('+', '')
            print('%s -%s: %s' % (' '*len(prog), o2, desc))
        print()
        sys.exit(1)

    def are_you_sure(self, msg=None):
        if msg:
            print(msg)
            print()
        print('Are you sure? ', end=' ')

        yn = sys.stdin.readline().strip().lower()
        if yn not in ('y', 'yes', 'yea', 'yeah', 'sure', 'si'):
            print('Existing')
            sys.exit(1)
        print()

    def emailResults(self, results, email_recipients):
        '''Email results to email_recipients'''

        from emailer import Emailer

        subject   = self._getEmailSubject()
        body_text = pretty(results)
        body_html = pretty(results, html=True)
        Emailer().send_email('internal', email_recipients, subject,
                             body_text, body_html)

    def _getEmailSubject(self):
        '''Return Email Subject line
           Format:
              [System-]Dla + Prog + Args (minus -e args)
        '''
        from vlib import conf

        conf_ = conf.getInstance()

         # prefix = conf.system name, unless it's Prod
        prefix = '' if conf_.system == 'prod' else conf_.system.title() + '-'

        # progname
        prog = os.path.basename(sys.argv[0]).replace('.py', '').title()

        # remove -e <email_list> from args
        p = self.evocation_args.index('-e')
        new_args = self.evocation_args[0:p] + self.evocation_args[p+2:]

        return '%sDla: %s %s' % (prefix, prog, ' '.join(new_args))

def pretty(results, html=False):
    '''Pretty format results
       Returns a string with \n's or <br/>'s
    '''

    LF = '\n'
    if html:
        LF = '<br/>\n'

    o = ''
    if results is None or results == '' or results == []:
        return o
    if isinstance(results, (list, tuple)):
        if isinstance(results[0], (list, tuple)):
            if html:
                from vweb.htmltable import HtmlTable
                table = HtmlTable(border=1, cellpadding=4, cellspacing=0)
            for row in results:
                row2 = []
                for cell in row:
                    if isinstance(cell, str) and ',' in cell:
                        row2.append('"%s"' % cell)
                    else:
                        row2.append(cell)
                if html:
                    table.addRow(map(str, row2))
                else:
                    o += ",".join(map(str, row2)) + LF
            if html:
                # hack in table style
                o = table.getTable().replace(
                    '<table cellpadding="4" cellspacing="0" border="1">',

                    '<style>tr td { border: 1px solid silver;}</style>'
                    '<table cellpadding="4" cellspacing="0" border="1" '
                    'style="font-size: 14px; border-collapse: collapse;">')
                return o
        else:
            o += "\n".join(map(str, results)) + LF
    elif isinstance(results, dict):
        keys = sorted(results.keys())
        for k in keys:
            o += "%s: %s" % (k, results[k]) + LF
    elif isinstance(results, int):
        o += str(results)
    elif isinstance(results, str):
        o += results.replace('\n', LF) + LF
    else:
        o += str(results)

    if html:
        o = o.replace('  ', ' &nbsp; ')

    return o.strip()

def print_pretty(results, html=False, use_pprint=0):
    '''Print to stdout pretty formated results'''
    if use_pprint:
        from pprint import pprint
        pprint(results)
    else:
        print(pretty(results, html))

class Test(object):
        
    def run(self):
        commands = ['say <greeting>',
                    'add <n> <m>',
                    'time']
        options = {'s+': '<bigcommerce_store_alias>'}
        self.cli = CLI(self.process, commands, options)
        return self.cli.process()

    def process(self, *args):
        '''Process incoming requests'''

        args = list(args)
        if len(args) < 1:
            self.cli.syntax('missing args')

        cmd = args.pop(0)
        if cmd == 'say':
            opt = args[0]
            return opt
        elif cmd == 'add':
            n = args[0]
            m = args[1]
            return str(int(n) + int(m))

        elif cmd == 'time':
            import datetime
            return str(datetime.datetime.now())

        else:
            raise CLI_Error('Unrecognized Command: %s' % cmd)

if __name__ == '__main__':
    Test().run()
