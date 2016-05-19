# !/usr/bin/env python
# -*- coding:utf-8 -*-

from base import Base, UTC
from datetime import datetime
from bs4 import BeautifulSoup
import urlparse

# 定义了网页抓取相关的方法，专门用于将一个排行榜类的网页转换为 Feed
class Feed(Base):

    oldest = 1

    def spider_get_post_href(self, soup):
        yield 'href'
    def spider_process_html(self, soup):
        html = unicode(soup.body)
        return html

    def spider_generate_html(self, result):
        for page, url in result:
            if not page: continue
            soup = self.process_article(page)
            html = self.spider_process_html(soup)
            if html: yield (html, url)

    def spider_refresh_capture(self, url, html):
        # return detect_url, set([capture_url])
        if html is None: return None, set()
        soup = BeautifulSoup(html, "lxml")
        capture = set()
        for href in self.spider_get_post_href(soup):
            capture.add(urlparse.urljoin(url, href))
        return None, capture

    def current_time(self):
        t = datetime.utcnow()
        return datetime(t.year, t.month, t.day, 0, 0, 0, tzinfo=UTC(0))

    def get_item(self):
        # yield title, time, link, content
        time = self.current_time()
        last_check = self.get_last_check()
        if last_check >= time:
            print '%s has captured today' % self.name
            return
        result = self.spider_main(detect = self.url)
        for html, url in self.spider_generate_html(result):
            yield self.name, time, url, html
        self.refresh_last_check(time)
