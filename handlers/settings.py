#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Main configuration file"""

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


# Main storage
# ------------
# db.urls = {
#   "_id" : 111,                                          # decode alphabet syms
#   "counter" : 1,                                        # url sha1 hash
#   "created" : ISODate("2013-12-11T10:09:08.765Z"),      # timestamp of creation
#   "creator" : {                                         # meta info about creator
#     "rroute" : [                                        # remote route
#       "127.0.0.1"
#     ],
#     "raddr" : "127.0.0.1",                              # remote IP address
#     "api" : false,                                      # API is used
#     "method" : "POST"                                   # HTTP method
#   },
#   "hash" : "4ef30e9f2fb32bc91fb1c0b5163e5d9b47bea1f0",  # url sha1 hash
#   "inaddr" : "http://t34.me",                           # input url
#   "lastreq" : ISODate("2014-11-10T09:08:07.654Z"),      # lastest request datetime
#   "outaddr" : "http://t34.me"                           # output (converted) url
# }

# Indexes:
# db.urls.ensureIndex({"hash": 1}, {"unique": 1})
# db.urls.ensureIndex({"lastreq": 1, "created": 1})
# db.urls.ensureIndex({"counter": -1})

# Storage for a lock
# ------------
# db.locks = {
#     "_id": 1,                                           # id is always 1
#     "threading": 3492394756                             # parent class ID
#     "status": ISODate("2014-10-10T09:08:07.654Z")       # date of creation
# }

# Indexes:
# db.locks.ensureIndex({"status": 1}, {expireAfterSeconds: 30})
