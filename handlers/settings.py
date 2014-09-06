#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Main configuration"""

import os
import logging.config
from json import load

VERSION = 'v0.8'

DEBUG = False
PRODUCTION = False

# real values can be defined in local_settings.py
ADMIN = 'admin@MY_SITE_NAME'
PREFIX = "http://MY_SITE_NAME"
DB = {
    "host": "localhost",
    "port": "27017",
    "user": "username",
    "password": "user_password",
    "database": "dbname",
    "authdb": "admin",
    "REPLICA": None
}

# Yandex metrika code
METRIKA = ""

# This dynamically discovers the path to the project
PROJECT_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), "..")
MEDIA = os.path.join(PROJECT_PATH, 'media')
LOGGING_CFG = 'logging.json'
LOGGING_FILE = '/tmp/t34.me.log'
LOGGING_CFG_PATH = os.path.join(PROJECT_PATH, 'configs', LOGGING_CFG)

assert os.path.isfile(LOGGING_CFG_PATH)

LOGGING_CFG = {}
with open(LOGGING_CFG_PATH, 'r') as logging_fd:
    LOGGING_CFG = load(logging_fd)
    LOGGING_CFG['handlers']['file']['filename'] = LOGGING_FILE

logging.config.dictConfig(LOGGING_CFG)

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SIMPLE_ALPHABET = '0123456789abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'

# IDs 1-99 are sererved for tests
MIN_ID = 100
# waiting of unclock, seconds
MAX_WAITING_LOCK = 20
# max attemps free-add url
FREE_ATTEMPS = 3
# days for statistics
STAT_DAYS = 7

# rewrite global setting vars
# Define in local_settings: DB, DEBUG, PREFIX, ADMIN
try:
    from handlers.local_settings import DB, DEBUG, PREFIX, ADMIN, PRODUCTION
except ImportError:
    print("Import error")

if DEBUG:
    LOGGER = logging.getLogger('debugMode')
else:
    LOGGER = logging.getLogger('rpoductionMode')

LOGGER.debug("mongo_db={0}".format(DB['database']))

# db.urls = {
#     "_id": 3244,                                          # _id => decode alphabet syms
#      "hash": "4a8a9fc31dc15a4b87bb145b05db3ae0bf2333e4"   # url sha1 hash
#     "inaddr": "https://www.google.ru/search?q=я"          # input url
#     "outaddr": "https://www.google.ru/search?q=%D1%8F"    # converted url
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
# db.urls.ensureIndex({"lastreq": 1, "created": 1})
# db.urls.ensureIndex({"counter": -1})

# db.locks = {
#     "_id": 1,
#     "threading": 3492394756                               # parent class ID
#     "status": date3                                       # date of creation
# }
# db.locks.ensureIndex({"status": 1}, {expireAfterSeconds: 30})
