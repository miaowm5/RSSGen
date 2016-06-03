# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, auth
from datetime import datetime, timedelta
from leancloud import Object, Query, LeanCloudError
from lib import PyRSS2Gen
import recipe

Feed = Object.extend('FeedItem')
FeedInfo = Object.extend('FeedInfo')
OnlineFeed = Object.extend('OnlineFeed')
DebugLog = Object.extend('DebugLog')

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
    except LeanCloudError, e: print "Save feed error: %s" % str(e)

def set_feed_data(name, data):
    item = Feed()
    item.set('name', name)
    item.set('title', data[0])
    item.set('time', data[1])
    item.set('link', data[2])
    item.set('content', data[3])
    save_data(item)

def save_rss(name, rss, info):
    count = 0
    for data in rss.get_item():
        count += 1
        set_feed_data(name, data)
    print('Spider %s, add %s new feed' % (name, count))
    if count > 0: save_data(info)
    if len(rss.log) == 0: return
    log = DebugLog()
    log.set('name', name)
    for key,value in rss.log: log.set(str(key), value)
    save_data(log)

def save(all_feed=False, feed_name=None):
    for r in rss_list(all_feed):
        name = r.name
        if feed_name and feed_name != name: continue
        info = get_info(name)
        rss = r(info=info)
        try: save_rss(name, rss, info)
        except Exception as e: print('save %s fail : %s' % (r.name, str(e)))

def rss_list(all_feed=False):
    if all_feed: return (set(recipe.recipe_list) | set(recipe.hide_list))
    else: return set(recipe.recipe_list)

def save_online(feed_name=None):
    feeds = Query(OnlineFeed).find()
    base = recipe.base_list
    for r in feeds:
        base_class = base.get(r.get('base'), None)
        if not base_class: continue
        name = 'ol-%s' % r.get('name')
        if feed_name and feed_name != name: continue
        info = get_info(name)
        rss = base_class(info=info)
        rss.set_online_recipe(r.get('data'))
        try: save_rss(name, rss, info)
        except Exception as e: print('save %s fail : %s' % (r.name, str(e)))

def online_rss_list():
    return [a.get('name') for a in Query(OnlineFeed).find()]

def get_all_feed(name):
    query = Query(Feed)
    query.equal_to('name', name).descending("time")
    return query.find()

def show(name):
    rss = PyRSS2Gen.RSS2(title=name,link="https://github.com/miaowm5",description="RSSGen By Miaowm5")
    for e in get_all_feed(name):
        title = e.get('title')
        time = e.get('time')
        time = datetime(*(time.utctimetuple()[0:6]))
        link = e.get('link')
        content = e.get('content')
        item = PyRSS2Gen.RSSItem(title=title,pubDate=time,
          link=link,description=content)
        rss.items.append(item)
    return rss.to_xml(encoding='utf-8')

def clear():
    for r in rss_list(all_feed=True): clear_feed(r.name, r.oldest)

def clear_online():
    for r in Query(OnlineFeed).find(): clear_feed('ol-%s' % r.get('name'), r.get('data')[4])

def clear_feed(name, day):
    oldest = datetime.now() - timedelta(days=day)
    query = Query(Feed)
    query.equal_to('name', name).less_than("time", oldest)
    for e in query.find():
        print('delete old feed: %s (%s)' % (e.get('title').encode('utf-8'), e.get('time')))
        e.destroy()

def add_online_feed(name, base, data):
    try: feed = Query(OnlineFeed).equal_to('name', name).first()
    except LeanCloudError, e:
        if e.code == 101:
            feed = OnlineFeed()
            feed.set('name', name)
        else: raise(e)
    feed.set('base', base)
    feed.set('data', data)
    feed.save()

def get_online_feed(name):
    try: feed = Query(OnlineFeed).equal_to('name', name).first()
    except LeanCloudError, e:
        if e.code == 101: return [name, '', None]
        else: raise(e)
    return [feed.get('name'), feed.get('base'), feed.get('data')]

def remove_online_feed(name):
    Query(OnlineFeed).equal_to('name', name).first().destroy()
    for e in Query(Feed).equal_to('name', 'ol-%s' % name).find(): e.destroy()