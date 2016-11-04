# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Hexieshe(Feed):
    name = 'hexieshe'
    url = r'http://www.xxshe.com/feed/'
    capture = {}
    capture["catch"] = [".entry-content"]
    capture["remove"] = [".wumii-hook",".pagination"]
    capture["nav"] = '.pagination > a'

recipe = Hexieshe