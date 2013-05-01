#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# This file contains base methods
import settings, datetime, re, pymongo, hashlib

t34dict = settings.ALPHABET
# t34dict = settings.SIMPLE_ALPHABET
basLen = len(t34dict)

CACHE_DEFAULT = hashlib.sha1().hexdigest()

class t34MongoEx(Exception):
    def __init__(self):
        self.value = "t34MongoEx: auth error for monogDB connection"
    def __str__(self):
        return repr(self.value)

class t34LockExt(Exception):
    def __init__(self):
        self.value = "t34LockExt: lock error for monogDB connection"
    def __str__(self):
        return repr(self.value)

class t34GenExt(Exception):
    def __init__(self):
        self.value = "t34GenExt: logic error of t34Url"
    def __str__(self):
        return repr(self.value)

# ------------
# Methods
# ------------
def mongo_connect():
    """connect to MongoDB database"""
    db = None
    try:
        connection = pymongo.MongoClient(host=settings.DB['host'], port=settings.DB['port'])
        db = connection[settings.DB["database"]]
        if not db.authenticate(settings.DB['user'], settings.DB['password']):
            return False
    except (pymongo.errors.OperationFailure,) as e:
        return False
    return db

def t34_decode(x, basis=basLen):
    """
    Convert any number basis-based to decimal:

    x - source string
    result - decimal number
    """
    global t34dict
    i, result = 0, 0
    syms = str(x)
    while syms:
        result += t34dict.index(syms[-1]) * (basis**i)
        syms = syms[:-1]
        i += 1
    return result

def t34_encode(x, basis=basLen):
    """
    Convert any number from decimal to basis-based

    x - decimal interger number
    result - converted string
    """
    global t34dict
    result = ""
    while x > 0:
        i = x % basis
        result = t34dict[i] + result
        x = x // basis
    return result

def std_decode(x, basis):
    """standart python converter any number basis-based to decimal"""
    if basis <= 36:
        result = int(str(x), basis)
        return result
    return None

# ------------
# Classes
# ------------
class t34Base(object):
    """docstring for t34Base"""
    def __init__(self):
        self.db = None
        self.connection()

    def connection(self):
        db = mongo_connect()
        if not db:
            raise t34MongoEx()
        self.db = db

class t34Url(t34Base):
    """
    It is a base class of t34.me

    shortID 1-100 are reserved for tests
    """
    def __init__(self, shortID=None):
        super(t34Url, self).__init__()
        self.data = None
        self.id = None if not shortID else t34_decode(shortID)
        self.get_data()

    def __repr__(self):
        return "<t34Url: {0}>".format(self.id)

    def __str__(self):
        return "<t34Url: {0}>".format(self.id)

    def __bool__(self):
        return bool(self.id)

    def get_data(self):
        self.col = self.db.urls
        if self.id:
            self.data = self.col.find_one({"_id": self.id})

    def add(self, fullurl):
        """add new url to DB storage"""
        hash = hashlib.sha1(fullurl.encode("utf-8")).hexdigest()

    def get_max(self):
        max_val = self.col.aggregate({"$group": {"_id": "max", "val": {"$max": "$_id"}}})
        if max_val["ok"]:
            result = 100 if max_val["result"][0]["val"] < 100 else max_val["result"][0]["val"]
            return int(result)
        else:
            raise t34GenExt()