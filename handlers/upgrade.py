#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Basic upgrade methods"""

from handlers.settings import LOGGER, ALPHABET, OLD_ALPHABET
from handlers.t34base import T34GenExt
from handlers.t34methods import T34Url
import asyncio
import hashlib
import datetime

UPGRADE1 = datetime.datetime(2015, 2, 13, 22, 0)

def upgrade1_conv(value, inv=False):
    """it convets old format to new one"""
    result = ""
    for val in value:
        if inv:
            result += OLD_ALPHABET[ALPHABET.find(val)]
        else:
            result += ALPHABET[OLD_ALPHABET.find(val)]
    return result

@asyncio.coroutine
def sync_handler_num2str(obj, item, test):
    """upgrade operation"""
    oldid = item.get("_id")
    item["_id"] = obj.t34_encode(int(oldid))
    item["hash"] = hashlib.sha1(item["outaddr"].encode("utf-8")).hexdigest()
    if not test:
        obj.delete(oldid)
        obj.collection.insert(item)
    else:
        if obj.upgrade({"_id": oldid}, {"$set": {"_id": item["_id"]}}, True) < 1:
            LOGGER.warning("not updated? old={0}, new={1}".format(oldid, item["_id"]))
    LOGGER.debug("old={0}, new={1}".format(oldid, item["_id"]))

def num2str(test=True):
    """Upgrade numeric ID to string-based values"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    obj = T34Url()
    try:
        for item in obj.collection.find({}):
            num = item.get("_id")
            if type(num) in (int, float):
                tasks.append(asyncio.async(sync_handler_num2str(obj, item, test)))
        LOGGER.debug("{0} tasks should be handled".format(len(tasks)))
        if tasks:
            loop.run_until_complete(asyncio.wait(tasks))
    except (T34GenExt,) as err:
        LOGGER.error(err)
        return 1
    finally:
        loop.close()
    return 0

@asyncio.coroutine
def sync_handler_save_upgrade1(obj, item, test):
    """add old field for an item"""
    if item.get("created") < UPGRADE1:
        newid = item.get("_id")
        oldid = upgrade1_conv(newid)
        res = obj.upgrade({"_id": newid}, {"$set": {"old": oldid}}, test)
        if res is None:
            LOGGER.error("Ivalid upgrade: {0}".format(newid))
        else:
            LOGGER.info("Valid upgrade: {0} / {1}".format(newid, oldid))

def save_upgrade1(test=True):
    """save old shortID to special field 'old'"""
    loop, tasks = asyncio.new_event_loop(), []
    asyncio.set_event_loop(loop)
    obj = T34Url()
    try:
        for item in obj.collection.find({"old": {"$exists": False}, "created": {"lt": UPGRADE1}}):
            if item.get("created"):
                tasks.append(asyncio.async(sync_handler_save_upgrade1(obj, item, test)))
        LOGGER.debug("{0} tasks should be handled".format(len(tasks)))
        if tasks:
            loop.run_until_complete(asyncio.wait(tasks))
    except (T34GenExt,) as err:
        LOGGER.error(err)
        return 1
    finally:
        loop.close()
    return 0
