'''Main dla Website App
   This is called by wsgi.py
'''
import os
import sys

from flask import Flask, request, Response, send_from_directory

app = Flask(__name__)

@app.route('/')
@app.route('/gallery/<id>')
def gallery(id=None):
    if not id:
        id = 1
    from gallery import GalleryPage
    return GalleryPage(id).go()

@app.route('/piece/<id>')
def piece(id):
    from piece import PiecePage
    return PiecePage(id).go()

@app.route('/show/<id>')
def show(id):
    from show import ShowPage
    return ShowPage(id).go()

@app.route('/about')
def about():
    from about import AboutPage
    return AboutPage().go()

@app.route('/contact')
def contact():
    from contact import ContactPage
    return ContactPage().go()

@app.route('/favicon.ico')
def favicon():
    '''TO DO: Set up favicon'''
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

from flask import render_template
@app.route('/hero_test')
def test_hero():
    from hero_test import HeroTest
    return HeroTest().go()

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
