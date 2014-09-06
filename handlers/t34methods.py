#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""This file contains base methods"""

import datetime
import time
import hashlib
import random
import re
import threading

from handlers.settings import ALPHABET, FREE_ATTEMPS, DEBUG, MAX_WAITING_LOCK, LOGGER, MIN_ID
from urllib.parse import urlparse, urlunparse, quote
from handlers.t34base import MongodbBase, T34GenExt, mongo_required
from pymongo.errors import ConnectionFailure, DuplicateKeyError

# try:
#     from urllib.parse import urlparse, urlunparse, quote
# except ImportError:
#     # deploy exception, don't need it for right python settings
#     from urlparse import urlparse, urlunparse
#     from urllib import quote

T34DICT = ALPHABET # or SIMPLE_ALPHABET
BAS_LEN = len(T34DICT)

CACHE_DEFAULT = hashlib.sha1().hexdigest()

URL_PREFIX = re.compile(r'^(.+)://', re.UNICODE)

# =========================== T34Lock ======================
class T34Lock(MongodbBase):
    """docstring for T34Lock"""
    def __init__(self, is_test=False):
        super(T34Lock, self).__init__()
        self._is_test = is_test
        self._locks = None
        self.init()

    @property
    def locks(self):
        return self._locks

    @mongo_required
    def __enter__(self):
        """lock operation before any actions"""
        self._locks = self._database.testlocks if self._is_test else self._database.locks
        now = datetime.datetime.utcnow
        end_time = now() + datetime.timedelta(seconds=MAX_WAITING_LOCK)
        thread = threading.currentThread().ident
        while now() < end_time:
            try:
                lock = self._locks.insert({"_id": 1, "thread": thread, "status": now()})
                if lock:
                    LOGGER.debug("Lock: id={0}".format(lock))
                    return 0
            except (DuplicateKeyError,) as err:
                LOGGER.info(err)
                time.sleep(0.5 + random.random())
            except (ConnectionFailure, AttributeError) as err:
                LOGGER.info(err)
                raise T34GenExt("Some problems")
        raise T34GenExt("Cannot lock")

    @mongo_required
    def __exit__(self, exp_type, exp_value, traceback):
        """unlock operation"""
        if not self._locks:
            self._locks = self._database.testlocks if self._is_test else self._database.locks
        thread = threading.currentThread().ident
        self._locks.remove({"thread": thread})
        return True

# =========================== T34Url ======================
class T34Url(MongodbBase):
    """
        The main app class to handle requests.
        ShortID 1-100 are reserved for the tests
    """
    def __init__(self, shortID=None, is_test=False):
        super(T34Url, self).__init__()
        self._is_test = is_test
        self._data, self._col, self._newest = None, None, False
        self._id = 0 if not shortID else self.t34_decode(shortID)
        self.init()
        self.get_data()

    def __repr__(self):
        return "<t34: {0}>".format(self._id)

    def __str__(self):
        return "<t34: {0}>".format(self._id)

    def __bool__(self):
        return bool(self._data)

    def __len__(self):
        if not self._data:
            return 0
        return len(self.t34_encode(self._data["_id"]))

    def __lt__(self, other):
        return self._id < other.id

    def __le__(self, other):
        return self._id <= other.id

    def __gt__(self, other):
        return self._id > other.id

    def __ge__(self, other):
        return self._id >= other.id

    def __eq__(self, other):
        return self._id == other.id

    def __ne__(self, other):
        return self._id != other.id

    def __hash__(self):
        return hash(id(self))

    @property
    def newest(self):
        """is it new item?"""
        return self._newest

    @property
    def data(self):
        """total info about an item"""
        return self._data

    @property
    def id(self):
        return self._id

    @staticmethod
    def t34_decode(xsource, basis=BAS_LEN):
        """Convert any number basis-based to decimal:

        PARAMS:
            xsource - source string
            result - decimal number
        """
        i, result = 0, 0
        syms = str(xsource)
        while syms:
            result += T34DICT.index(syms[-1]) * (basis**i)
            syms = syms[:-1]
            i += 1
        return result

    @staticmethod
    def t34_encode(xsource, basis=BAS_LEN):
        """Convert any number from decimal to basis-based

        PARAMS:
            xsource - decimal interger number
            result - converted string
        """
        result = ""
        while xsource > 0:
            i = xsource % basis
            result = T34DICT[i] + result
            xsource = xsource // basis
        return result

    @staticmethod
    def url_prepare(link):
        """prepares url string. By default, all links are not secured."""
        link = link.strip()
        try:
            if not URL_PREFIX.findall(link):
                link = "http://" + link
            templ = urlparse(link)
            new_url = {
                "scheme": templ.scheme,
                "netloc": templ.netloc.encode('idna').decode('utf-8'),
                "path": quote(templ.path.encode("utf-8"), safe="%/:=&?~#+!$,;'@()*[]"),
                "query": quote(templ.query.encode("utf-8"), safe="%/:=&?~#+!$,;'@()*[]"),
                "params": quote(templ.params.encode("utf-8"), safe="%/:=&?~#+!$,;'@()*[]"),
                "fragment": quote(templ.fragment.encode("utf-8"), safe="%/:=&?~#+!$,;'@()*[]"),
            }
            result = urlunparse((new_url["scheme"], new_url["netloc"], new_url["path"], new_url["params"], new_url["query"], new_url["fragment"]))
        except (ValueError, TypeError, IndexError) as err:
            LOGGER.warning("can not parse url: {0}".format(err))
            result = ""
        return result

    # @mongo_required
    def get_data(self):
        """soft check of connection, w/o exception"""
        if self.connected:
            self._col = self._database.urls
            if self._is_test:
                self._col = self._database.tests
            if self._id:
                self._data = self._col.find_one({"_id": self._id})
            return 0
        return 1

    @mongo_required
    def clean(self):
        """delete all data, only for the test mode"""
        assert self._is_test
        self._col.remove({})

    @mongo_required
    def refresh(self):
        """refresh data about url"""
        if self._id:
            self._data = self._col.find_one({"_id": self._id})

    @mongo_required
    def reset(self, full_url):
        """reset data about url"""
        self._id, self._data = 0, None
        self.create(full_url)

    @mongo_required
    def create(self, full_url):
        """try to add url id DB"""
        if self._create_free(full_url):
            return self.t34_encode(self._id)
        return None

    def _create_free(self, full_url):
        """Adds new url to DB storage, in free mode."""
        uhash = hashlib.sha1(full_url.encode("utf-8")).hexdigest()
        created = False
        for i in range(FREE_ATTEMPS):
            already = self._col.find_one({"hash": uhash})
            if already:
                self._id, self._data = already["_id"], already
                return True
            now = datetime.datetime.utcnow()
            try:
                obj = {
                    '_id': self._get_max(),
                    'hash': uhash,
                    'inaddr': full_url,
                    'counter': 0,
                    'created': now,
                    'lastreq': now,
                    'outaddr': self.url_prepare(full_url)
                }
                created = self._col.insert(obj)
                if created:
                    self._id, self._data, self._newest = obj["_id"], obj, True
                    return True
            except (DuplicateKeyError,) as err1:
                LOGGER.info("DuplicateKeyError, attempt={0}".format(i))
                LOGGER.debug(err1)
                time.sleep(0.1 + random.random())
            except (ConnectionFailure, AttributeError) as err2:
                LOGGER.info(err2)
                raise T34GenExt("Some problems during item creation")
        return self._create_lock(full_url)

    def _create_lock(self, full_url):
        """Creare a new url link in locked mode."""
        with T34Lock(self._is_test):
            uhash = hashlib.sha1(full_url.encode("utf-8")).hexdigest()
            try:
                already = self._col.find_one({"hash": uhash})
                if already:
                    self._id, self._data = already["_id"], already
                    return True
                now = datetime.datetime.utcnow()
                obj = {
                    '_id': self._get_max(),
                    'hash': uhash,
                    'inaddr': full_url,
                    'counter': 0,
                    'created': now,
                    'lastreq': now,
                    'outaddr': self.url_prepare(full_url)
                }
                created = self._col.insert(obj)
                if created:
                    self._id, self._data, self._newest = obj["_id"], obj, True
                    return True
            except (ConnectionFailure, AttributeError) as err:
                LOGGER.warning(err)
                raise T34GenExt()
        # can't lock DB, unachievable code
        return False

    @mongo_required
    def delete(self, num=None, short_url=None, full_url=None):
        """delete item using different variants"""
        result = False
        if num:
            result = self._col.remove({"_id": num})
        elif short_url:
            result = self.t34_decode(short_url)
            result = self._col.remove({"_id": result})
        elif full_url:
            result = hashlib.sha1(full_url.encode("utf-8")).hexdigest()
            result = self._col.remove({"hash": result})
        if result:
            return bool(result["ok"])
        return False

    def _get_max(self):
        """gets max ID number+1"""
        result = 10 if DEBUG else MIN_ID
        try:
            max_val = self._col.aggregate({"$group": {"_id": "max", "val": {"$max": "$_id"}}})
            if max_val.get('ok') != 1:
                raise T34GenExt()
            if max_val.get('result') and max_val["result"][0]["val"]:
                result = result if max_val["result"][0]["val"] < result else max_val["result"][0]["val"]
        except (ConnectionFailure, AttributeError, IndexError) as err:
            LOGGER.error(err)
            raise T34GenExt()
        return result + 1

    def update(self):
        """update existed data"""
        if self._id:
            try:
                result = self._col.update({"_id": self._id}, {"$set": {"lastreq": datetime.datetime.utcnow()}, "$inc": {"counter": 1}})
                if result["updatedExisting"]:
                    self.refresh()
                    return True
            except (ConnectionFailure, AttributeError) as err:
                LOGGER.debug(err)
                raise T34GenExt()
        LOGGER.debug("item not found")
        return False

    def complement(self, compl_data):
        """set additional info for an item"""
        if self._id:
            try:
                result = self._col.update({"_id": self._id}, {"$set": {"creator": compl_data}})
                if result["updatedExisting"]:
                    # self.refresh()
                    self._data["creator"] = compl_data
                    return True
            except (ConnectionFailure, AttributeError) as err:
                LOGGER.error(err)
                raise T34GenExt()
        return False