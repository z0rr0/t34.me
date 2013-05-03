#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# This file contains base methods
import settings, datetime, time, pymongo, hashlib, random, urllib, re, threading

t34dict = settings.ALPHABET
# t34dict = settings.SIMPLE_ALPHABET
basLen = len(t34dict)

CACHE_DEFAULT = hashlib.sha1().hexdigest()

class t34MongoEx(Exception):
    def __init__(self):
        self.value = "t34MongoEx: auth error for monogDB connection"
    def __str__(self):
        return repr(self.value)

# class t34LockExt(Exception):
#     def __init__(self):
#         self.value = "t34LockExt: lock error for monogDB connection"
#     def __str__(self):
#         return repr(self.value)

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
    except (pymongo.errors.OperationFailure, pymongo.errors.ConnectionFailure) as e:
        raise t34MongoEx()
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

def url_prepare(link):
    # for national domains
    link = link.strip()
    prefix = re.compile(r'^(.+)://', re.UNICODE)
    try:
        if not prefix.findall(link):
            link = "http://" + link
        templ = urllib.parse.urlparse(link)
        q = urllib.parse.quote
        new_url = {
            "scheme": templ.scheme,
            "netloc": templ.netloc.encode('idna').decode('utf-8'),
            "path": q(templ.path, safe="%/:=&?~#+!$,;'@()*[]"),
            "query": q(templ.query, safe="%/:=&?~#+!$,;'@()*[]"),
            "params": q(templ.params, safe="%/:=&?~#+!$,;'@()*[]"),
            "fragment": q(templ.fragment, safe="%/:=&?~#+!$,;'@()*[]"),
        }
        result = urllib.parse.urlunparse((new_url["scheme"], new_url["netloc"], new_url["path"], new_url["params"], new_url["query"], new_url["fragment"]))
    except (Exception,) as e:
        result = ""
    return result

# ------------
# Classes
# ------------
class t34Base(object):
    """docstring for t34Base"""
    def __init__(self, shortID=None):
        self.db = None
        self.id = 0 if not shortID else t34_decode(shortID)
        self.connection()

    def connection(self):
        try:
            db = mongo_connect()
            if db:
                self.db = db
        except (t34MongoEx,) as e:
            pass

    def __repr__(self):
        return "<t34: {0}>".format(self.id)

    def __str__(self):
        return "<t34: {0}>".format(self.id)

    def __bool__(self):
        return bool(self.data)

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(id(self))


class t34Url(t34Base):
    """
    It is a base class of t34.me

    shortID 1-100 are reserved for tests
    """
    def __init__(self, shortID=None, isTest=False):
        super(t34Url, self).__init__(shortID)
        self.data = None
        self.get_data(isTest)

    def get_data(self, isTest=False):
        if self.db:
            self.col = self.db.urls
            self.locks = self.db.locks
            if isTest:
                self.col = self.db.tests
                self.locks = self.db.testlocks
            if self.id:
                self.data = self.col.find_one({"_id": self.id})

    def refresh(self):
        if self.db and self.id:
            self.data = self.col.find_one({"_id": self.id})

    def reset(self, fullUrl):
        self.id, self.data = 0, None
        self.create(fullUrl)

    def create(self, fullUrl):
        if self.db is None:
            raise t34GenExt()
        if self.create_free(fullUrl):
            return t34_encode(self.id)
        return None

    def create_free(self, fullUrl):
        """
        Add new url to DB storage, in free mode
        """
        uhash = hashlib.sha1(fullUrl.encode("utf-8")).hexdigest()
        created = False
        for i in range(settings.FREE_ATTEMPS):
            already = self.col.find_one({"hash": uhash})
            if already:
                self.id, self.data = already["_id"], already
                return True
            now = datetime.datetime.utcnow()
            try:
                obj = {"_id": self.get_max(),
                    "hash": uhash, "inaddr": fullUrl, "counter": 0,
                    "created": now, "lastreq": now, 'outaddr': url_prepare(fullUrl)}
                created = self.col.insert(obj)
                if created:
                    self.id, self.data = obj["_id"], obj
                    return True
            except (pymongo.errors.DuplicateKeyError,) as e:
                # the unsuccessful attempt
                time.sleep(0.1 + random.random())
        return self.create_lock(fullUrl)

    def create_lock(self, fullUrl):
        """
        Creare new url link in locked mode
        """
        if self.lock(True):
            # DB is locked
            uhash = hashlib.sha1(fullUrl.encode("utf-8")).hexdigest()
            already = self.col.find_one({"hash": uhash})
            if already:
                self.id, self.data = already["_id"], already
                return True
            now = datetime.datetime.utcnow()
            try:
                obj = {"_id": self.get_max(),
                        "hash": uhash, "inaddr": fullUrl, "counter": 0,
                        "created": now, "lastreq": now, 'outaddr': url_prepare(fullUrl)}
                created = self.col.insert(obj)
                if created:
                    self.id, self.data = obj["_id"], obj
                    return True
            except (pymongo.errors.ConnectionFailure,) as e:
                raise t34GenExt()
        # can't lock DB
        return False

    def delete(self, num=None, shortUrl=None, fullUrl=None):
        result = False
        if num:
            result = self.col.remove({"_id": num})
        elif shortUrl:
            result = t34_decode(shortUrl)
            result = self.col.remove({"_id": result})
        elif fullUrl:
            result = uhash = hashlib.sha1(fullUrl.encode("utf-8")).hexdigest()
            result = self.col.remove({"hash": result})
        if result:
            return bool(result["ok"])
        return False

    def lock(self, state=False):
        """state: True - lock, False - unlock"""
        now = datetime.datetime.utcnow
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.MAX_WAITING_LOCK)
        thread = threading.currentThread().ident
        if state:
            while (now() < end_time):
                try:
                    lock = self.locks.insert({"_id": 1, "thread": thread, "status": now()})
                    if lock: return True
                except (pymongo.errors.DuplicateKeyError,) as e:
                    # print(e)
                    time.sleep(0.5 + random.random())
            return False
        else:
            self.locks.remove({"thread": thread})
        return True

    def get_max(self):
        max_val = self.col.aggregate({"$group": {"_id": "max", "val": {"$max": "$_id"}}})
        if settings.DEBUG:
            min_val = 10
        else:
            min_val = settings.MIN_ID
        if max_val["ok"]:
            if max_val["result"]:
                result = min_val if max_val["result"][0]["val"] < min_val else max_val["result"][0]["val"]
                return int(result + 1)
            else:
                return min_val
        else:
            raise t34GenExt()

    def update(self):
        if self:
            try:
                result = self.col.update({"_id": self.id}, {"$set": {"lastreq": datetime.datetime.utcnow()}, "$inc": {"counter": 1}})
                if result["updatedExisting"]:
                    self.refresh()
                    return True
            except (pymongo.errors.ConnectionFailure,) as e:
                raise t34GenExt()
        return False

    def complement(self, compl_data):
        if self.id:
            try:
                result = self.col.update({"_id": self.id}, {"$set": {"creator": compl_data}})
                if result["updatedExisting"]:
                    # self.refresh()
                    self.data["creator"] = compl_data
                    return True
            except (pymongo.errors.ConnectionFailure,) as e:
                raise t34GenExt()
        return False
