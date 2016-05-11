# !/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib, urllib2, datetime
from lib import feedparser
from bs4 import BeautifulSoup

class Base(object):

    name = 'Feed Name'
    url = 'Detect URL'

    def __init__(self, info):
        self.info = info

    def featch_url(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        result = urllib2.urlopen(urllib2.Request(url=url,headers=headers))
        if result.getcode() == 200: return result.read()
        else:
            print('Featch URL Fail(%s): %s' % url, result.getcode())
            return None

    def featch_content(self, url):
        content = self.featch_url(url)
        if content: content = content.decode("utf-8")
        return content

    def spider_main(self, detect = None, capture = set()):
        detect  = detect
        capture = capture
        done    = set()
        cache   = {}
        result  = []
        task = capture if detect is None else (set([detect]) | capture)
        task = task - done
        while len(task) > 0:
            for url in task:
                cache[url] = None
                content = self.featch_content(url)
                if content: cache[url] = content
                else: print('Fetch URL failed, skip(%s)' % url)
            for url in capture:
                if not url in done: result.append( (cache.get(url, None), url) )
            spider = self.spider_refresh_capture(detect, cache.get(detect, None))
            if len(spider) >= 3:
                if spider[2]: result.append( (cache.get(detect, None), detect) )
            detect, capture = spider[0], spider[1]
            done.add(url)
            cache = {}
            task = capture if detect is None else (set([detect]) | capture)
            task = task - done
        return result

    def spider_refresh_capture(self, url, html):
        # return detect_url, set([capture_url])[, add_detect_to_result]
        if html is None: return None, set()
        capture = set()
        return None, capture

    def convert_time(self, time):
        return datetime.datetime(*(time[0:6]))

    def get_last_check(self):
        last_check = self.info.get('check')
        return self.convert_time(last_check.timetuple())

    def refresh_last_check(self, time):
        self.info.set('check', time)

    def get_item(self):
        # yield title, time, link, content
        pass

class Feed(Base):

    def get_feed_time(self,e):
        update = None
        if hasattr(e, 'published_parsed') and e.published_parsed: update = e.published_parsed
        elif hasattr(e, 'updated_parsed') and e.updated_parsed: update = e.updated_parsed
        elif hasattr(e, 'created_parsed'): update = e.created_parsed
        if update: update = self.convert_time(update)
        return update

    def get_item(self):
        # yield title, time, link, content
        content = self.featch_url(self.url)
        if not content: return
        content = feedparser.parse(content)
        last_check = self.get_last_check()
        last_update = self.get_feed_time(content.feed)
        if last_update and last_check >= last_update:
            print '%s has no update after last spider' % self.name
            return
        for title, time, link, describe in self.create_item(content['entries']):
            if last_check >= time: break
            yield title, time, link, describe
        self.refresh_last_check(last_update)

    def create_item(self, feed):
        for e in feed:
            title = e.title
            link = e.link
            time = self.get_feed_time(e)
            describe = title
            yield title, time, link, describe
