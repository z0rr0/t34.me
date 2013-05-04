#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# This file contains main handlers of web pages
# please look https://developers.google.com/safe-browsing/

import os, pymongo, settings, bottle
from t34methods import *

@bottle.get('/')
def index():
    return bottle.template('index')

@bottle.post('/')
def result():
    value = bottle.request.forms.t34url
    if not value.strip():
        bottle.redirect("/")
    try:
        obj = t34Url()
        result = settings.PREFIX + obj.create(value)
        mdict = {"api": False,
            "method": bottle.request.method,
            "raddr": bottle.request.remote_addr,
            "rroute": bottle.request.remote_route}
        obj.complement(mdict)
    except (t34GenExt,) as e:
        raise HTTPError(500)
    return bottle.template('result', var=result)

@bottle.get('/<link:re:[0-9a-zA-Z]+>')
def prepare(link):
    if settings.DEBUG:
        print("prepare", link)
    try:
        obj = t34Url(link)
        if obj:
            obj.update()
            if obj.data["outaddr"]:
                bottle.redirect(obj.data['outaddr'])
            # javasctipt - it's very simple variant
            return bottle.template('redirect', url=obj.data['inaddr'])
    except (t34GenExt, pymongo.errors.ConnectionFailure) as e:
        raise HTTPError(500)
    raise bottle.HTTPError(404)

@bottle.route('/api/')
def api():
    if bottle.request.query.u:
        try:
            obj = t34Url()
            result = settings.PREFIX + obj.create(bottle.request.query.u)
            mdict = {"api": True,
                "method": bottle.request.method,
                "raddr": bottle.request.remote_addr,
                "rroute": bottle.request.remote_route}
            obj.complement(mdict)
            if bottle.request.query.web:
                return bottle.template('result', var=result)
        except (t34GenExt,) as e:
            return "Error"
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
    return bottle.static_file(filename, root=settings.MEDIA)

@bottle.route('/about/')
def about():
    views = os.path.join(settings.PROJECT_PATH, 'views')
    return bottle.static_file("about.html", root=views)

bottle.TEMPLATE_PATH.insert(0, os.path.join(settings.PROJECT_PATH, 'views'))
if settings.DEBUG:
    bottle.run(host='0.0.0.0', port=28080, debug=True, reloader=True)
else:
    bottle.TEMPLATES.clear()
