#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# basic tests
import random, settings, t34methods

ESTR = "a" if settings.DEBUG else "1C"

def test_prepate():
    try:
        db = t34methods.mongo_connect()
    except (t34methods.t34MongoEx,) as e:
        return
    db.tests.remove()
    db.testlocks.remove()

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
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_mongo():
    test_name = "test_mongo"
    print("\nTest '{0}' is started...".format(test_name))
    try:
        db = t34methods.mongo_connect()
    except (t34methods.t34MongoEx,) as e:
        print("Test '{0}' is not passed".format(test_name))
        return 1
    if db:
        urls = db.urls
        print("test value: {0}".format(urls.find_one()))
        print("Test '{0}' is passed".format(test_name))
    else:
        print("Test '{0}' is not passed".format(test_name))
        return 1
    return 0

def test_urlobj():
    test_name = "test_urlobj"
    print("\nTest '{0}' is started...".format(test_name))
    obj = t34methods.t34Url(None, True)
    try:
        if settings.DEBUG:
            print("{0}, get_max={1}".format(obj, obj.get_max()))
        assert(str(obj) == "<t34: 0>")
    except (AssertionError, t34methods.t34GenExt) as e:
        print(str(obj))
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_locks():
    test_name = "test_locks"
    print("\nTest '{0}' is started...".format(test_name))
    obj = t34methods.t34Url(None, True)
    try:
        obj.lock(True)
        if settings.DEBUG:
            print(obj.locks.find_one())
        obj.lock(False)
        assert(obj.locks.find_one() == None)
    except (AssertionError, t34methods.t34GenExt) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_obj_creation():
    """for test _id=10=a"""
    global ESTR
    test_name = "test_obj_creation"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = t34methods.t34Url(None, True)
    try:
        result = obj.create(test_url)
        assert(result == ESTR)
        if settings.DEBUG:
            print(obj.data)
        assert(obj.delete(None, None, test_url) == True)
    except (AssertionError, t34methods.t34GenExt) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_obj_deletion():
    """for test _id=10=a"""
    global ESTR
    test_name = "test_obj_deletion"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = t34methods.t34Url(None, True)
    try:
        # by num
        result = obj.create(test_url)
        assert(result == ESTR)
        key = obj.id
        assert(obj.delete(key) == True)
        # by short url
        result = obj.create(test_url)
        assert(result == ESTR)
        assert(obj.delete(None, result) == True)
        # by full url
        result = obj.create(test_url)
        assert(result == ESTR)
        assert(obj.delete(None, None, test_url) == True)
    except (AssertionError, t34methods.t34GenExt) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_double_create():
    global ESTR
    test_name = "test_double_create"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = t34methods.t34Url(None, True)
    try:
        result1 = obj.create(test_url)
        assert(result1 == ESTR)
        result2 = obj.create(test_url)
        assert(result2 == ESTR)
        if settings.DEBUG:
            print(obj.data)
        obj2 = t34methods.t34Url(None, True)
        result3 = obj2.create(test_url)
        assert(obj == obj2)
        assert(result3 == result2)
        assert(obj.delete(None, None, test_url) == True)
        assert(obj2.delete(None, None, test_url) == True)
    except (AssertionError, t34methods.t34GenExt) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_update_counter():
    test_name = "test_update_counter"
    global ESTR
    print("\nTest '{0}' is started...".format(test_name))
    max_in_test = 10
    test_url = "http://t34.me"
    obj = t34methods.t34Url(None, True)
    try:
        result = obj.create(test_url)
        assert(result == ESTR)
        assert(obj.data["counter"] == 0)
        assert(obj.update() == True)
        for i in range(max_in_test - 1):
            obj.update()
        assert(obj.data["counter"] == max_in_test)
        if settings.DEBUG:
            print(obj.data)
        assert(obj.delete(None, None, test_url) == True)
    except (AssertionError, t34methods.t34GenExt) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_url_converter():
    test_name = "test_url_converter"
    print("\nTest '{0}' is started...".format(test_name))
    utls = (
        ("http://t34.me", "http://t34.me"),
        ("президент.рф", "http://xn--d1abbgf6aiiy.xn--p1ai"),
        ("https://президент.рф/визиты", "https://xn--d1abbgf6aiiy.xn--p1ai/%D0%B2%D0%B8%D0%B7%D0%B8%D1%82%D1%8B"),
        ("https://google.com/?search=я", "https://google.com/?search=%D1%8F"),
        ("http://randomsite.com/paragraph#map1", "http://randomsite.com/paragraph#map1"),
        ("http://randomsite.com/параграф#map1", "http://randomsite.com/%D0%BF%D0%B0%D1%80%D0%B0%D0%B3%D1%80%D0%B0%D1%84#map1"),
        ("dddd", "http://dddd")
    )
    obj = t34methods.t34Url(None, True)
    try:
        for url in utls:
            if settings.DEBUG:
                print("check: {0} <==> {1}".format(t34methods.url_prepare(url[0]), url[1]))
            assert(t34methods.url_prepare(url[0]) == url[1])
    except (AssertionError,) as e:
        print(e, "Test '{0}' is not passed".format(test_name))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

if __name__ == '__main__':
    total, er = 0, 0
    test_prepate()
    if test_converter(2):
        er += 1
    total += 1
    if test_mongo():
        er += 1
    total += 1
    if test_urlobj():
        er += 1
    total += 1
    if test_locks():
        er += 1
    total += 1
    if test_obj_creation():
        er += 1
    total += 1
    if test_obj_deletion():
        er += 1
    total += 1
    if test_double_create():
        er += 1
    total += 1
    if test_update_counter():
        er += 1
    total += 1
    if test_url_converter():
        er += 1
    total += 1
    print("\nThe test result: total={0}, with error={1}, passed={2}".format(total, er, total-er))