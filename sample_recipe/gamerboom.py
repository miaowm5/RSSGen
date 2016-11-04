# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Gamerboom(Feed):
    name = 'gamerboom'
    url = r'http://gamerboom.com/feed'
    capture = {}
    capture["catch"] = ['div.cnt_body']

recipe = Gamerboom