'''Main dla Website App
   This is called by wsgi.py
'''
import os
import sys

from flask import Flask, request, Response, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    from home import HomePage
    return HomePage().go()

@app.route('/gallery/<id>', methods=['GET', 'POST'])
def gallery(id=None):
    if not id:
        id = 1
    from gallery import GalleryPage
    return GalleryPage(id).go()

@app.route('/piece/<id>')
def piece(id):
    from piece import PiecePage
    return PiecePage(id).go()

@app.route('/shows')
def shows():
    from shows_page import ShowsPage
    return ShowsPage().go()

@app.route('/show/<id>')
def show(id):
    from show import ShowPage
    return ShowPage(id).go()

@app.route('/collections')
def collections():
    from collections_page import CollectionsPage
    return CollectionsPage().go()

@app.route('/about')
def about():
    from about import AboutPage
    return AboutPage().go()

@app.route('/contact')
def contact():
    from contact import ContactPage
    return ContactPage().go()

@app.errorhandler(404)
def page_not_found(e):
    from page_not_found import PageNotFoundPage
    return PageNotFoundPage().go()

@app.route('/favicon.ico')
def favicon():
    '''TO DO: Set up favicon'''
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
# Not for production
#@app.route("/showenv")
def showenv():
    o = '<h1>Environment</h1>'

    # python
    o += '<h2>python</h2>'
    o += '<table>'
    o += '<tr><td>executable</td><td>%s</td></tr>' % sys.executable
    o += '<tr><td>version</td><td>%s</td></tr>' % sys.version
    o += '</table>'

    # headers
    o += '<h2>request.headers</h2>'
    o += '<table>'
    for k,v in request.headers:
        o += '<tr><td>%s</td><td>%s</td></tr>' % (k, v)
    o += '</table>'

    # env
    o += '<h2>os.environ</h2>'
    o += '<table>'
    for k in sorted(os.environ.keys()):
        if k in (['DDB_PASS']):
            continue
        v = os.environ[k]
        o += '<tr><td>%s</td><td>%s</td></tr>' % (k, v)
    o += '</table>'

    return f'<div style="padding: 10px">{o}</div>'

# One method to handle them all using eval()
# def page(id=None):
#     if request.url_rule.rule == '/':
#         page = 'gallery'
#         id = 1
#     else:
#         page = request.url_rule.rule.split('/')[1]
#     module = __import__(page, globals(), locals())
#     class_name = '%sPage' % snake2camel(page)
#     page_output = eval(f'getattr(module, "{class_name}")({id}).go()')
#     return page_output
