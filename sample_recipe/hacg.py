# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Hacg(Feed):
    name = 'hacg'
    url = r'http://www.hacg.li/wp/feed'
    capture = {}
    capture["catch"] = ['.entry-content',]
    capture["remove"] = ['.page-link',]
    capture["nav"] = '.page-link > a'

recipe = Hacg