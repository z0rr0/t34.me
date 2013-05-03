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
        print(e, "\nERROR: please use date format YYYY-mm-dd, now your incorrect date: {0}".format(opts.date))
        return
    print("Max counter:")
    counter_stat(opts.records, date)
    # print("\nMax request from address:")
    # radd_stat(opts.records, date)

def counter_stat(num, start):
    try:
        db = t34methods.mongo_connect()
        col = db.urls
        results = col.find({"lastreq": {"$gte": start}}).sort([("counter", pymongo.DESCENDING), ("lastreq", pymongo.ASCENDING)]).limit(num)
    except (t34methods.t34MongoEx, AttributeError) as e:
        print(e)
        print("ERROR: problem with mongoDB connect")
        return
    i = 1
    template = "ID={0}, short=http://t34.me/{6}\n\tcounter={1}, creator={2}, api={5}\n\tlastreq={3}, created={4}"
    if results.count():
        print("Top:")
    for res in results:
        print(i, template.format(res["_id"], res["counter"], res["creator"]["raddr"], res["lastreq"], res["created"], res["creator"]["api"], t34methods.t34_encode(res["_id"])))
        i += 1
    return 0

def radd_stat(num, start):
    try:
        db = t34methods.mongo_connect()
        col = db.urls
        results = col.aggregate([{"$match": {"lastreq": {"$gte": start}}}, {"$group": {"_id": "$creator.raddr", "sum": {"$sum": 1}, "ids": {"$addToSet" : "$_id" }}}, {"$sort": {"sum": -1}}, {"$limit": num}])
    except (t34methods.t34MongoEx, AttributeError) as e:
        print(e)
        print("ERROR: problem with mongoDB connect")
        return
    if results["ok"]:
        i = 1
        template = "{0}  tIP={1}, sum links={2}\n\t{3}"
        for res in results['result']:
            print(template.format(i, res["_id"], res["sum"], res["ids"]))
            i += 1
    else:
        print("incorrect aggregare request")

if __name__ == '__main__':
    main()