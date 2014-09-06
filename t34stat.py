#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""Info about statistics"""

import optparse
import datetime
import pymongo

from handlers.settings import STAT_DAYS, LOGGER, PREFIX
from handlers.t34base import MongodbBase, MongoEx, mongo_required
from handlers.t34methods import T34Url

class T34Stat(MongodbBase):
    """docstring for T34Stat"""
    def __init__(self):
        super(T34Stat, self).__init__()
        self._col = None
        self.init()
        if self.connected:
            self._col = self._database.urls

    @mongo_required
    def total(self):
        """returns total number of objects"""
        return self._col.find().count() if self._col else 0

    @mongo_required
    def counter_stat(self, num, start):
        """statistics"""
        results = []
        if self._col:
            results = self._col.find({"lastreq": {"$gte": start}}).sort([("counter", pymongo.DESCENDING), ("lastreq", pymongo.ASCENDING)]).limit(num)
        return results

def main():
    """main method"""
    now = datetime.datetime.utcnow()
    start_date = now.date() + datetime.timedelta(days=-STAT_DAYS)

    parser = optparse.OptionParser()
    parser.add_option("-r", "--records", dest="records", type="int", default=True, help=("maximum records for statistics [default: %default]"))
    parser.add_option("-d", "--date", dest="date", type="string", default=True, help=("date start [default: %default]"))

    parser.set_defaults(records=20, date=start_date.strftime("%Y-%m-%d"))
    opts, args = parser.parse_args()
    try:
        date = datetime.datetime.strptime(opts.date, "%Y-%m-%d")
    except (ValueError,) as err:
        LOGGER.info("\nERROR: {1} please use date format YYYY-mm-dd, now your incorrect date: {0}".format(opts.date, err))
        return
    print("Max counter:")
    counter_stat(opts.records, date)

def counter_stat(num, start):
    """print statistics"""
    try:
        obj = T34Stat()
        if not obj.connected:
            LOGGER.error("Cannot connect to MongoDB")
        total = obj.total()
        results = obj.counter_stat(num, start)
    except (MongoEx, AttributeError) as err:
        LOGGER.error(err)
        return 1
    i = 1
    print("total links: {0}".format(total))
    template = "ID={0}, short={7}{6}\n\tcounter={1}, creator={2}, api={5}\n\tlastreq={3}, created={4}"
    if results.count():
        print("Top:")
    for res in results:
        print(i, template.format(res["_id"], res["counter"], res["creator"]["raddr"], res["lastreq"], res["created"], res["creator"]["api"], T34Url.t34_encode(res["_id"]), PREFIX))
        i += 1
    return 0

if __name__ == '__main__':
    main()
