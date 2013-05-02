#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# This file contains main handlers of web pages
# please look https://developers.google.com/safe-browsing/

import os, settings, bottle
from t34methods import *

# ToDo
# prefix
# national domains
# national encoding

@bottle.get('/')
def index():
    return bottle.template('index')

@bottle.post('/')
def result():
    global PREFIX
    value = bottle.request.forms.t34url
    try:
        obj = t34Url()
    except (t34GenExt,) as e:
        raise HTTPError(500)
    result = settings.PREFIX + obj.create(value)
    mdict = {"api": False,
        "method": bottle.request.method,
        "raddr": bottle.request.remote_addr,
        "rroute": bottle.request.remote_route}
    obj.complement(mdict)
    return bottle.template('result', var=result)

@bottle.get('/<link:re:[0-9a-zA-Z]+>')
def prepare(link):
    if settings.DEBUG:
        print("prepare", link)
    try:
        obj = t34Url(link)
    except (t34GenExt,) as e:
        raise HTTPError(500)
    if obj:
        obj.update()
        # to use this function our shourld to parse url - url_prepare():
        # national domain; national url; username/password/port and etc...
        if obj.data["encfull"]:
            bottle.redirect(obj.data['encfull'])
        # javasctipt - it's very simple variant
        return bottle.template('redirect', url=obj.data['full'])
    # forum_id = bottle.request.query.id
    raise bottle.HTTPError(404)

@bottle.route('/api')
def api():
    if bottle.request.query.u:
        try:
            obj = t34Url()
        except (t34GenExt,) as e:
            return "Error"
        result = settings.PREFIX + obj.create(bottle.request.query.u)
        mdict = {"api": True,
            "method": bottle.request.method,
            "raddr": bottle.request.remote_addr,
            "rroute": bottle.request.remote_route}
        obj.complement(mdict)
        return result
    else:
        bottle.redirect("/")

@bottle.error(404)
def error404(error):
    return bottle.template('404')

@bottle.error(500)
def error500(error):
    return bottle.template('500')

@bottle.route('/media/<filename:path>')
def media(filename):
    global MEDIA
    return bottle.static_file(filename, root=settings.MEDIA)

@bottle.route('/about/')
def about():
    views = os.path.join(settings.PROJECT_PATH, 'views')
    print(views)
    return bottle.static_file("about.html", root=views)

@bottle.route('/about/')
def about():
    views = os.path.join(settings.PROJECT_PATH, 'views')
    print(views)
    return bottle.static_file("about.html", root=views)

bottle.TEMPLATES.clear()
if settings.DEBUG:
    bottle.run(host='localhost', port=28080, debug=True, reloader=True)
else:
    bottle.TEMPLATES.clear()
