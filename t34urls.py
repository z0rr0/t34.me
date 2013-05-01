#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# This file contains main handlers of web pages
# please look https://developers.google.com/safe-browsing/

import os, settings, bottle

MEDIA = os.path.join(settings.PROJECT_PATH, 'media')

@bottle.get('/')
def index():
    return bottle.template('index', content="Ok")

@bottle.route('/<name:re:[0-9a-zA-Z]+>')
def index2(name='World'):
    forum_id = bottle.request.query.id
    name2 = bottle.request.forms.name
    return bottle.template('<b>Hello {{name}}</b>!!! f={{ fid }} <a href="/media/empty">aaa</a>', name=name, fid=forum_id)

@bottle.error(404)
def error404(error):
    return 'Nothing here, sorry'

@bottle.route('/yandex/')
def wrong():
    bottle.redirect("http://ya.ru")

def is_ajax():
    if bottle.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    else:
        return False

@bottle.route('/media/<filename:path>')
def media(filename):
    global MEDIA
    return bottle.static_file(filename, root=MEDIA)

if settings.DEBUG:
    bottle.run(host='localhost', port=28080, debug=True, reloader=True)
else:
    bottle.TEMPLATES.clear()
