# !/usr/bin/env python
# -*- coding:utf-8 -*-

from base import Base
from lib import feedparser

# 定义了 Feed 需要的相关方法，用于将非全文 RSS 转换为全文 RSS 的类
class Feed(Base):

    def get_last_update(self, content):
        return self.get_feed_time(content.feed)

    def get_feed_time(self,e):
        update = None
        if hasattr(e, 'published_parsed') and e.published_parsed: update = e.published_parsed
        elif hasattr(e, 'updated_parsed') and e.updated_parsed: update = e.updated_parsed
        elif hasattr(e, 'created_parsed'): update = e.created_parsed
        if update: update = self.convert_time(update)
        return update

    def get_item(self):
        # yield title, time, link, content
        content = self.featch_content(self.url)
        if not content: return
        content = feedparser.parse(content)
        last_check = self.get_last_check()
        last_update = self.get_last_update(content)
        if last_update and last_check >= last_update:
            print '%s has no update after last spider' % self.name
            return
        for title, time, link, content in self.create_item(content['entries']):
            if not last_update: last_update = time
            if last_check >= time: break
            yield title, time, link, content
        self.refresh_last_check(last_update)

    def create_item(self, feed):
        for e in feed:
            title = e.title
            link = e.link
            time = self.get_feed_time(e)
            describe = self.create_content(link)
            yield title, time, link, describe

    def create_content(self, url):
        result = self.spider_main(detect=url, capture=set([url]))
        content = self.spider_generate_html(result)
        return content
