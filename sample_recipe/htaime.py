# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Htaime(Feed):
    name = 'htaime'
    oldest = 1
    url = r'http://htai.me/feed'
    capture = {}
    capture["catch"] = ['div.post_content']
    capture["remove"] = ['#author_profile', ".single_free_space"]
    capture["block_img"] = ['alicdn']

recipe = Htaime