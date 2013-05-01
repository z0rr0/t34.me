#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# basic tests
import random, settings, t34methods

def test_converter(limit=10):
    test_name = "test_converter"
    print("\nTest '{0}' is started...".format(test_name))
    a, b = 1e2, 1e6
    i = 0
    try:
        while i < limit:
            x1 = random.randint(a, b)
            x2 = t34methods.t34_encode(x1)
            if settings.DEBUG:
                print("{0} == {1}".format(x2, x1))
            assert(t34methods.t34_decode(x2) == x1)
            i +=1
    except (AssertionError,) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return
    print("Test '{0}' is passed".format(test_name))

def test_mongo():
    test_name = "test_mongo"
    print("\nTest '{0}' is started...".format(test_name))
    db = t34methods.mongo_connect()
    if db:
        urls = db.urls
        print("test value: {0}".format(urls.find_one()))
        print("Test '{0}' is passed".format(test_name))
    else:
        print("Test '{0}' is not passed".format(test_name))

def test_urlobj():
    test_name = "test_urlobj"
    print("\nTest '{0}' is started...".format(test_name))
    obj = t34methods.t34Url()
    try:
        if settings.DEBUG:
            print("{0}, get_max={1}".format(obj, obj.get_max()))
        assert(str(obj) == "<t34: 0>")
    except (AssertionError,) as e:
        print(str(obj))
        print(e, "Test '{0}' is not passed".format(test_name))
        return
    print("Test '{0}' is passed".format(test_name))

def test_locks():
    test_name = "test_locks"
    print("\nTest '{0}' is started...".format(test_name))
    obj = t34methods.t34Url()
    try:
        obj.lock(True)
        if settings.DEBUG:
            print(obj.locks.find_one())
        obj.lock(False)
        assert(obj.locks.find_one() == None)
    except (AssertionError,) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return
    print("Test '{0}' is passed".format(test_name))

if __name__ == '__main__':
    test_converter(2)
    test_mongo()
    test_urlobj()
    test_locks()