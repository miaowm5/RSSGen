# !/usr/bin/env python
# -*- coding:utf-8 -*-

from rank_base import Feed

class Danbooru(Feed):
    name = 'Danbooru'
    url = r'http://danbooru.donmai.us/explore/posts/popular'
    capture = {}
    capture["catch"] = ["#image-container"]

    def spider_get_post_href(self, soup):
        for e in soup.find_all('article'): yield e.a['href']
    def spider_process_html(self, soup):
        dom = soup.select('img')
        if len(dom) == 0: return None
        return '<img src="%s" />' % dom[0]['src']

recipe = Danbooru