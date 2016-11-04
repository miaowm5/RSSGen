# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed2_base import Feed

class Dm178(Feed):
    name = '178dm'
    oldest = 1
    capture = {}
    capture["block_img"] = ['159502145898']
    url = r'http://acg.178.com/s/rss.xml'

recipe = Dm178