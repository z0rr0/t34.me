#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os

ADMIN = "admin@t34.me"
DEBUG = True

DB = {
    "host": "",
    "port": "",
    "user": "",
    "password": ""
}

# This dynamically discovers the path to the project
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SIMPLE_ALPHABET = '0123456789abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'

# IDs 1-99 are sererved for tests
MIN_ID = 100
# waiting of unclock, seconds
MAX_WAITING_LOCK = 20
# max attemps free-add url
FREE_ATTEMPS = 3

# rewrite global setting vars
try:
    from local_settings import *
except ImportError:
    pass


# db.urls = {
#     "_id": 3244,                                          # _id => decode alphabet syms
#      "hash": "4a8a9fc31dc15a4b87bb145b05db3ae0bf2333e4"   # url sha1 hash
#     "full": "http://yandex.ru",                           # url
#     "counter": 2,                                         # increment counter of requests
#     "created": date1,                                     # creation datetime
#     "lastreq": date2,                                     # last request datetime
#     "creator": {
#       "raddr": "192.168.0.1",
#       "rroute": ["192.168.0.1"],
#       "method": "GET",
#       "api": false,
#   }
# }
# db.urls.ensureIndex({"hash": 1}, {"unique": 1})
# db.urls.ensureIndex({"created": 1, "lastreq": 1})
# db.urls.ensureIndex({"counter": -1})

# db.locks = {
#     "_id": 1,
#     "threading": 3492394756                               # thread ID
#     "status": date3                                       # date of creation
# }
# db.locks.ensureIndex({"status": 1}, {expireAfterSeconds: 30})
