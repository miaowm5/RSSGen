# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class ACGPiPing(Feed):
    name = 'acgpiping'
    url = r'http://www.acgpiping.net/feed/'
    capture = {}
    capture["catch"] = ['.post_content']
    capture["remove"] = ['.wumii-hook','.WPSNS_main']
    oldest = 5

recipe = ACGPiPing