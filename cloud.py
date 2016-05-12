# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, auth, datetime
from leancloud import Object, Query
import spider

Feed = Object.extend('FeedItem')

def spider_work():
    spider.save()
    print('spider work at %s' % datetime.datetime.now())

def clear_old_feed():
    for e in Query(Feed).find():
        time = datetime.datetime(*(e.get('time').timetuple()[0:6]))
        day = (datetime.datetime.now() - time).days
        if day > 1:
            print('delete old feed:%s(%s)' % (e.get('title').encode('utf-8'), time))
            e.destroy()
