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

# rewrite global setting vars
try:
    from local_settings import *
except ImportError:
    pass

# db.urls = {
#     "_id": 3244,                                          # _id => alphabet syms
#      "hash": "4a8a9fc31dc15a4b87bb145b05db3ae0bf2333e4"   # url sha1 hash
#     "full": "http://yandex.ru",                           # url
#     "created": date1,
#     "modified": date2,
# }
