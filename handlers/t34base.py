#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Base MongoDB classes
"""

from handlers.settings import LOGGER, DB
from pymongo import MongoReplicaSetClient, MongoClient
from pymongo.errors import OperationFailure, ConnectionFailure
from pymongo.read_preferences import ReadPreference
import datetime
from functools import lru_cache, wraps

# ------------------------------+
# Basic mongo connection class  |
# ------------------------------+
class MongodbBase(object):
    """docstring for MongodbBase"""
    def __init__(self):
        """init MongodbBase"""
        super(MongodbBase, self).__init__()
        self._database = None
        self._connection = None

    def init(self):
        """open database connection"""
        self._connect()

    def _connect(self):
        """mongodb connect"""
        cfg = DB.get("REPLICA")
        try:
            if cfg:
                self._connection = MongoReplicaSetClient(host=cfg["host"], port=cfg["port"], replicaSet=cfg["id"], read_preference=ReadPreference.SECONDARY_PREFERRED)
            else:
                self._connection = MongoClient(host=DB['host'], port=DB['port'], read_preference=ReadPreference.PRIMARY)
            authdb = DB.get('authdb', DB["database"])
            self._database = self._connection[DB["database"]]
            if not self._database.authenticate(DB['user'], DB['password'], source=authdb):
                LOGGER.error("MongodbBase auth error")
                return False
        except (OperationFailure, ConnectionFailure) as err:
            LOGGER.error("MongodbBase connection error: {0}".format(err))
            return False
        return True

    @property
    def connected(self):
        """returns connect boolean value"""
        return self._connection.alive() if self._connection else False

    @property
    def database(self):
        """returns database object"""
        return self._database

    def __del__(self):
        """close mongodb connection"""
        if self.connected:
            try:
                self._database.connection.close()
            except (AttributeError, OperationFailure, ConnectionFailure) as err:
                LOGGER.warning(err)
            self._connected = False

# ------------------------------+
# Basic exceptions              |
# ------------------------------+
class MongoEx(Exception):
    """mongoDB exception class"""

    def __init__(self):
        super(MongoEx, self).__init__()
        self._value = "MongoEx: auth/connect error of MongoDB"

    def __str__(self):
        return repr(self._value)

class T34GenExt(Exception):
    """general app exception"""

    def __init__(self, value=None):
        super(T34GenExt, self).__init__()
        value = value if value else "logic error"
        self._value = "t34GenExt: {0}".format(value)

    def __str__(self):
        return repr(self._value)

class StripPathMiddleware(object):
    """WSGI middleware that strips trailing slashes from all URLs"""
    def __init__(self, app):
        """init method"""
        self.app = app

    def __call__(self, var1, var2):
        """strip slashes"""
        var1['PATH_INFO'] = var1['PATH_INFO'].rstrip('/')
        return self.app(var1, var2)

# ------------------------------+
# Basic decorators              |
# ------------------------------+
def debug_profiler(function):
    """used to get profilling data"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        """decorator wrapper"""
        start = datetime.datetime.now()
        result = function(*args, **kwargs)
        LOGGER.debug("Execution time of [{0}] = {1}\n".format(function.__name__, datetime.datetime.now() - start))
        return result
    return wrapper

def mongo_required(function):
    """validates mongo connection, applicable only for MongodbBase objects"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        """internal wrapper"""
        this = args[0]
        if not this.connected:
            LOGGER.error("can not connect to MongoDB")
            raise MongoEx()
        return function(*args, **kwargs)
    return wrapper

# ------------------------------+
# Methods                       |
# ------------------------------+
@lru_cache(32)
def std_decode(xsource, basis):
    """standart python converter any number basis-based to decimal"""
    if basis <= 36:
        result = int(str(xsource), basis)
        return result
    return None
