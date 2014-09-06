#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Internal tests"""


import random

from handlers.settings import DEBUG, LOGGER
from handlers.t34methods import T34Url, T34Lock
from handlers.t34base import MongoEx, T34GenExt

ESTR = "b" if DEBUG else "1D"

def test_prepate():
    """prepare env for tests"""
    try:
        testobj = T34Url(None, True)
        testobj.clean()
    except (MongoEx,) as err:
        LOGGER.error("Cannot connect to database: {0}".format(err))
    LOGGER.debug("Test preparion is finished.")

def test_converter(limit=10):
    """test basic converter methods"""
    test_name = "test_converter"
    print("\nTest '{0}' is started...".format(test_name))
    left, right = 1e2, 1e6
    i = 0
    try:
        while i < limit:
            source1 = random.randint(left, right)
            source2 = T34Url.t34_encode(source1)
            LOGGER.debug("{0} == {1}".format(source2, source1))
            assert T34Url.t34_decode(source2) == source1
            i += 1
    except (AssertionError,) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_mongo():
    """test mongodb connection"""
    test_name = "test_mongo"
    print("\nTest '{0}' is started...".format(test_name))
    try:
        testobj = T34Url(None, True)
        assert testobj.connected
    except (MongoEx, AssertionError) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_urlobj():
    """test object name"""
    test_name = "test_urlobj"
    print("\nTest '{0}' is started...".format(test_name))
    obj = T34Url(None, True)
    try:
        LOGGER.debug("{0}".format(obj))
        assert str(obj) == "<t34: 0>"
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_locks():
    """test lock mode"""
    test_name = "test_locks"
    print("\nTest '{0}' is started...".format(test_name))
    try:
        with T34Lock(True) as obj:
            one = obj.locks.find_one()
            LOGGER.debug(one)
            assert one['_id'] == 1
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_obj_creation():
    """for test _id=10=a"""
    test_name = "test_obj_creation"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = T34Url(None, True)
    try:
        result = obj.create(test_url)
        assert result == ESTR
        assert obj.delete(None, None, test_url) == True
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_obj_deletion():
    """for test _id=11=b"""
    test_name = "test_obj_deletion"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = T34Url(None, True)
    try:
        # by num
        result = obj.create(test_url)
        assert result == ESTR
        key = obj.id
        assert obj.delete(key) == True
        # by short url
        result = obj.create(test_url)
        assert result == ESTR
        assert obj.delete(None, result) == True
        # by full url
        result = obj.create(test_url)
        assert result == ESTR
        assert obj.delete(None, None, test_url) == True
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_double_create():
    """comparation of two objects"""
    test_name = "test_double_create"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://t34.me"
    obj = T34Url(None, True)
    try:
        result1 = obj.create(test_url)
        assert result1 == ESTR
        result2 = obj.create(test_url)
        assert result2 == ESTR
        # 2nd object
        obj2 = T34Url(None, True)
        result3 = obj2.create(test_url)
        assert obj == obj2
        assert result3 == result2
        assert obj.delete(None, None, test_url) == True
        assert obj2.delete(None, None, test_url) == True
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_update_counter():
    """check counter inside the object"""
    test_name = "test_update_counter"
    print("\nTest '{0}' is started...".format(test_name))
    max_in_test = 10
    test_url = "http://t34.me"
    obj = T34Url(None, True)
    try:
        result = obj.create(test_url)
        assert result == ESTR
        assert obj.data["counter"] == 0
        assert obj.update() == True
        for i in range(max_in_test - 1):
            obj.update()
        assert obj.data["counter"] == max_in_test
        assert obj.delete(None, None, test_url) == True
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_url_converter():
    """test some urls"""
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
    try:
        for url in utls:
            LOGGER.debug("check: {0} <==> {1}".format(url[0], url[1]))
            assert T34Url.url_prepare(url[0]) == url[1]
    except (AssertionError,) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
        return 1
    print("Test '{0}' is passed".format(test_name))
    return 0

def test_obj_newest():
    """for test _id=11=a"""
    test_name = "test_obj_newest"
    print("\nTest '{0}' is started...".format(test_name))
    test_url = "http://google.com/123"
    obj = T34Url(None, True)
    try:
        result = obj.create(test_url)
        assert result == ESTR
        assert obj.newest == True
        obj2 = T34Url(None, True)
        result = obj2.create(test_url)
        assert obj2.newest == False
        assert obj.delete(None, None, test_url) == True
        assert obj2.delete(None, None, test_url) == True
    except (AssertionError, T34GenExt) as err:
        LOGGER.warning("Test '{0}' is not passed: {1}".format(test_name, err))
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
    if test_obj_newest():
        er += 1
    total += 1
    print("\nThe test result: total={0}, with error={1}, passed={2}".format(total, er, total-er))
