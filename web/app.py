'''Main dla Website App
   This is called by wsgi.py
'''
import os
import sys

from flask import Flask, request, Response, send_from_directory

app = Flask(__name__)

@app.route('/', defaults={'id': 1})
@app.route('/gallery/<int:id>')
def gallery(id):
    from gallery import GalleryPage
    return GalleryPage(id).go()

@app.route('/piece/<int:id>')
def piece(id):
    from piece import PiecePage
    return PiecePage(id).go()

@app.route('/show/<int:id>')
def show(id):
    from show import ShowPage
    return ShowPage(id).go()

# @app.route('/')
# @app.route('/<page>', methods=['GET', 'POST'])
# def view(page=None):
#     '''General page view

#        Each URL <page> maps to a web.<page> python module, and then
#        the <page>Page class is instanciated and then
#        its go() method is then called.

#        eq.:
#           /about causes this to happens:

#              from about imoprt AboutPage
#              AboutPage().go()
#     '''
#     #setEnvVars()

#     # / => home page
#     if not page:
#         page = 'home'

#     # dynamically load and call the page
#     module = __import__(page, globals(), locals())
#     class_name = '%sPage' % snake2camel(page)
#     return eval('getattr(module, "%s")().go()' % class_name)

@app.route('/favicon.ico')
def favicon():
    '''TO DO: Set up favicon'''
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
