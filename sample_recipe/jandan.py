# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Jandan(Feed):
    name = 'jandan'
    url = r'http://jandan.net/feed'
    capture = {}
    capture["catch"] = ['div.post.f']
    capture["remove"] = ['h1','h3','.comment-big','.share-links','.star-rating','.jandan-zan']

    def process_image(self, img):
        url = img['data-original'] if 'data-original' in img.attrs else None
        if url: img['src'] = url

recipe = Jandan