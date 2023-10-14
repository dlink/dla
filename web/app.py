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

@app.route('/favicon.ico')
def favicon():
    '''TO DO: Set up favicon'''
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
