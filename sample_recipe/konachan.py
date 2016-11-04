# !/usr/bin/env python
# -*- coding:utf-8 -*-

from rank_base import Feed

class Konachan(Feed):
    name = 'konachan'
    url = r'http://konachan.net/post/popular_recent'
    capture = {}
    capture["catch"] = [".content .image"]

    def spider_get_post_href(self, soup):
        for e in soup.select(".thumb"): yield e['href']
    def spider_process_html(self, soup):
        dom = soup.select('img')
        if len(dom) == 0: return None
        return '<img src="%s" />' % dom[0]['src']

recipe = Konachan