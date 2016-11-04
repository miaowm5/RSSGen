# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Iplaysoft(Feed):
    name = 'iplaysoft'
    url = r'http://feed.iplaysoft.com'
    capture = {}
    capture["catch"] = ['div.entry-banner','div.entry-content']

recipe = Iplaysoft