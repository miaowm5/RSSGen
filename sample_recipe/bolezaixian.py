# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class BoLeZaiXian(Feed):
    name = 'bolezaixian'
    url = r'http://web.jobbole.com/feed/'
    capture = {}
    capture["catch"] = ['.entry']
    capture["remove"] = ['.copyright-area','#single-page-inner-widget','.post-adds','#author-bio','.crayon-main']

recipe = BoLeZaiXian