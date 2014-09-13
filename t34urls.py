#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Main file"""

import os
import bottle
import qrcode

from handlers.settings import LOGGER, PROJECT_PATH, PRODUCTION, MEDIA, PREFIX
from handlers.t34base import T34GenExt, MongoEx, StripPathMiddleware #, debug_profiler
from handlers.t34methods import T34Url

from io import BytesIO
from functools import lru_cache

@bottle.get('/')
@lru_cache(2)
def index():
    """index page"""
    return bottle.template('index')

@bottle.post('/')
def result():
    """create/update an item for icoming URL address"""
    value = bottle.request.forms.longurl
    if not value.strip():
        bottle.redirect("/")
    try:
        obj = T34Url()
        returned_link = obj.create(value)
        if not returned_link:
            LOGGER.warning("can not add link: {0}".format(value))
            raise T34GenExt()
        result_link = PREFIX + returned_link
        if obj.newest:
            obj.complement({
                "api": False,
                "method": bottle.request.method,
                "raddr": bottle.request.remote_addr,
                "rroute": bottle.request.remote_route
            })
    except (T34GenExt, MongoEx) as err:
        LOGGER.warning(err)
        raise bottle.HTTPError(500)
    return bottle.template('result', var=result_link, dirty=returned_link)

@bottle.get('/<link:re:[0-9a-zA-Z]+>')
@lru_cache(128)
def prepare(link):
    """return sreal URL by a short one"""
    try:
        obj = T34Url(link)
        if obj:
            obj.update()
            if obj.data.get('outaddr'):
                bottle.redirect(obj.data['outaddr'])
            # javasctipt - it's very simple variant
            LOGGER.warning("redirect by incoming address: id={0}".format(obj.data.get('_id')))
            return bottle.template('redirect', url=obj.data['inaddr'])
    except (T34GenExt, MongoEx) as err:
        LOGGER.warning(err)
        raise bottle.HTTPError(500)
    raise bottle.HTTPError(404)

@bottle.route('/api')
def api():
    """API request"""
    if bottle.request.query.u:
        try:
            obj = T34Url()
            returned_link = obj.create(bottle.request.query.u)
            if returned_link is None:
                LOGGER.warning("can not add link: {0}".format(bottle.request.query.u))
                raise T34GenExt()
            result_link = PREFIX + returned_link
            if obj.newest:
                obj.complement({
                    "api": True,
                    "method": bottle.request.method,
                    "raddr": bottle.request.remote_addr,
                    "rroute": bottle.request.remote_route
                })
            if bottle.request.query.web:
                return bottle.template('result', var=result_link, dirty=returned_link)
        except (T34GenExt, MongoEx) as err:
            LOGGER.error(err)
            bottle.response.status = 500
            result_link = "Error"
        return result_link
    else:
        bottle.redirect("/")

@bottle.error(404)
@lru_cache(2)
def error404(error):
    """HTTP error 404"""
    LOGGER.debug(error.status)
    return bottle.template('404')

@bottle.error(500)
@lru_cache(2)
def error500(error):
    """HTTP error 500"""
    LOGGER.debug(error.status)
    return bottle.template('500')

@bottle.get('/media/<filename:path>')
def media(filename):
    """paths for media content"""
    return bottle.static_file(filename, root=MEDIA)

@bottle.get('/about')
@lru_cache(2)
def about():
    """about page"""
    views = os.path.join(PROJECT_PATH, 'views')
    return bottle.static_file("about.html", root=views)

@bottle.get('/qrcode/<code>')
@lru_cache(128)
def getqrcode(code):
    """get QRcode"""
    if not bottle.request.query.d:
        result_link = PREFIX + code
    else:
        result_link = code
    qrc = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=6,
        border=2
    )
    qrc.add_data(result_link)
    qrc.make(fit=True)
    img = qrc.make_image()
    buf = BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    bottle.response.content_type = 'image/png'
    return buf.read()

bottle.TEMPLATE_PATH.insert(0, os.path.join(PROJECT_PATH, 'views'))
bottle.TEMPLATES.clear()

if not PRODUCTION:
    testapp = StripPathMiddleware(bottle.app())
    bottle.run(app=testapp, host='127.0.0.1', port=28080, debug=True, reloader=True)
else:
    application = StripPathMiddleware(bottle.default_app())
