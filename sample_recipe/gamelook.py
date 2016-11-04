# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Gamelook(Feed):
    name = 'gamelook'
    url = r'http://www.gamelook.com.cn/feed'
    capture = {}
    capture["catch"] = ['div.entry-content']
    capture["remove"] = ['#wp_rp_first']

recipe = Gamelook