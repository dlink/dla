'''Main dla Website App
   This is called by wsgi.py
'''
import os
import sys

from flask import Flask, request, Response, send_from_directory

app = Flask(__name__)

@app.route('/')
@app.route('/<page>', methods=['GET', 'POST'])
def view(page=None):
    '''General page view

       Each URL <page> maps to a web.<page> python module, and then
       the <page>Page class is instanciated and then
       its go() method is then called.

       eq.:
          /about causes this to happens:

             from about imoprt AboutPage
             AboutPage().go()
    '''
    setEnvVars()

    # / => home page
    if not page:
        page = 'home'

    # dynamically load and call the page
    module = __import__(page, globals(), locals())
    class_name = '%sPage' % snake2camel(page)
    page_output = eval('getattr(module, "%s")().go()' % class_name)
    return responseType(page_output, page)

def responseType(page_output, page_name):
    '''Generic handling for returning Response objects
       Returns HTML or csv files depending on DOCTYPE
    '''
    # html
    if page_output.startswith('<!DOCTYPE html'):
        return page_output

    # csv (\uFEFF is for excel utf8)
    return Response(
        u'\uFEFF' + page_output,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=%s.csv" % page_name})

@app.route('/favicon.ico')
def favicon():
    '''TO DO: Set up favicon'''
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

def setEnvVars():
    for row in open('/home/dlink/.dla', 'r').readlines():
        row = row.strip()
        export, parameters = row.split(' ')
        key, value = parameters.split('=')
        value = value.replace("'", '')
        os.environ[key] = value

def snake2camel(name):
    '''Eq.: convert smale_pieces to smallPieces'''
    parts = name.split('_')
    camel = ''.join(x.title() for x in parts)
    return camel
