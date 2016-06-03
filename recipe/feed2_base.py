# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed as Base

# 定义了 Feed 需要的相关方法，用于将其他网站的全文 RSS 转存到服务器

class Feed(Base):

    def create_item(self, feed):
        for e in feed:
            title = e.title
            link = e.link
            time = self.get_feed_time(e)
            summary = e.summary if hasattr(e, 'summary') else ""
            content = e.content[0]['value'] if (hasattr(e, 'content') and e.content[0]['value']) else ""
            html = content if len(content) > len(summary) else summary
            soup = self.process_article(html)
            describe = unicode(soup.body)
            yield title, time, link, describe

recipe = Feed