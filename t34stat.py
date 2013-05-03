#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# statistics
import optparse, datetime, settings, pymongo, t34methods

def main():
    now  = datetime.datetime.utcnow()
    start_date = now.date() + datetime.timedelta(days=-settings.STAT_DAYS)

    parser = optparse.OptionParser()
    parser.add_option("-r", "--records", dest="records", type="int", default=True,
        help=("maximum records for statistics [default: %default]"))
    parser.add_option("-d", "--date", dest="date",  type="string", default=True,
        help=("date start [default: %default]"))

    parser.set_defaults(records=20, date=start_date.strftime("%Y-%m-%d"))
    opts, args = parser.parse_args()
    try:
        date = datetime.datetime.strptime(opts.date, "%Y-%m-%d")
    except (ValueError,) as e:
        print(e)
        print("ERROR: please use date format YYYY-mm-dd, now your incorrect date: {0}".format(opts.date))
        return
    get_stat(opts.records, date)

def get_stat(num, start):
    db = t34methods.mongo_connect()
    if not db:
        print("ERROR: problem with mongoDB connect")
        return
    col = db.urls
    results = col.find({"lastreq": {"$gte": start}}).sort([("counter", pymongo.DESCENDING), ("lastreq", pymongo.ASCENDING)]).limit(num)
    i = 1
    template = "ID={0}, short=http://t34.me/{6}\n\tcounter={1}, creator={2}, api={5}\n\tlastreq={3}, created={4}"
    if results.count():
        print("Top:")
    for res in results:
        print(i, template.format(res["_id"], res["counter"], res["creator"]["raddr"], res["lastreq"], res["created"], res["creator"]["api"], t34methods.t34_encode(res["_id"])))
        i += 1


if __name__ == '__main__':
    main()