# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, auth
from datetime import datetime, timedelta
from leancloud import Object, Query, LeanCloudError
from lib import PyRSS2Gen
import recipe

Feed = Object.extend('FeedItem')
FeedInfo = Object.extend('FeedInfo')

def get_info(name):
    query = Query(FeedInfo).equal_to('name', name)
    try: info = query.first()
    except LeanCloudError, e:
        if e.code == 101:
            info = FeedInfo()
            info.set('name', name)
        else: raise(e)
    return info

def save_data(data):
    try: data.save()
    except LeanCloudError, e: print e

def save():
    for r in rss_list():
        name = r.name
        info = get_info(name)
        rss = r(info=info)
        for title, time, link, content in rss.get_item():
            item = Feed()
            item.set('name', name)
            item.set('title', title)
            item.set('time', time)
            item.set('link', link)
            item.set('content', content)
            save_data(item)
        save_data(info)

def rss_list():
    return recipe.recipe_list

def get_all_feed(name):
    query = Query(Feed)
    query.equal_to('name', name).descending("time")
    return query.find()

def show(name):
    rss = PyRSS2Gen.RSS2(title=name,link="https://github.com/miaowm5",description="RSSGen By Miaowm5")
    for e in get_all_feed(name):
        title = e.get('title')
        time = e.get('time')
        link = e.get('link')
        content = e.get('content')
        item = PyRSS2Gen.RSSItem(title=title,pubDate=time,
          link=link,description=content)
        rss.items.append(item)
    return rss.to_xml(encoding='utf-8')

def clear():
    for r in rss_list():
        name = r.name
        oldest = datetime.now() - timedelta(days=r.oldest)
        remove = []
        feed = get_all_feed(name)
        feed.reverse()
        for e in feed:
            time = datetime(*(e.get('time').timetuple()[0:6]))
            if (oldest - time).days > 0: remove.append(e)
            else: break
        for e in remove:
            print('delete old feed: %s (%s)' % (e.get('title').encode('utf-8'), e.get('time')))
            e.destroy()