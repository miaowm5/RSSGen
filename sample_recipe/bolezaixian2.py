# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class BoLeZaiXian2(Feed):
    name = 'bolezaixian2'
    url = r'http://python.jobbole.com/feed/'
    capture = {}
    capture["catch"] = ['.entry']
    capture["remove"] = ['.copyright-area','#single-page-inner-widget','.post-adds','#author-bio','.crayon-main']

recipe = BoLeZaiXian2