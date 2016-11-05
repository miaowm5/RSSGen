# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Pixivision(Feed):
    name = 'Pixivision'
    url = r'http://www.pixivision.net/zh/rss'
    capture = {}
    capture["catch"] = ['.am__body']
    capture["remove"] = ['.am__work__user-icon-container','.aie__uesr-icon']

recipe = Pixivision
