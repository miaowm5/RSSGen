# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed2_base import Feed

class JPbeta(Feed):
    name = 'jpbeta'
    url = r'http://www.jpbeta.net/feed/'
    capture = {}
    capture["remove"] = ['.wumii-related-items']

recipe = JPbeta