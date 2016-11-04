# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed
from datetime import timedelta

class Youxiputao(Feed):
    name = 'youxiputao'
    url = r'http://youxiputao.com/feed'
    capture = {}
    capture["catch"] = ['.pin-container .cover','.pin-container .info']

    def get_feed_time(self,e):
        time = super(Youxiputao, self).get_feed_time(e)
        return time + timedelta(seconds=28800)

    def get_last_update(self, content):
        time = super(Youxiputao, self).get_last_update(content)
        return time - timedelta(seconds=28800)

recipe = Youxiputao