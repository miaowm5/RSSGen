# !/usr/bin/env python
# -*- coding:utf-8 -*-

from rank_base import Feed

class Banciyuan(Feed):
    name = 'banciyuan'
    url = r'http://bcy.net/illust/toppost100?type=lastday'
    capture = {}
    capture["catch"] = [".detail_std"]

    def spider_get_post_href(self, soup):
        for e in soup.select(".work-thumbnail__topBd > a"): yield e['href']
    def spider_process_html(self, soup):
        dom = soup.select('img')
        if len(dom) == 0: return None
        for e in dom: return '<img src="%s" />' % e['src'].replace("/w650", '')

recipe = Banciyuan