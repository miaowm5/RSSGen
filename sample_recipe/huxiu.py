# !/usr/bin/env python
# -*- coding:utf-8 -*-

from feed_base import Feed

class Huxiu(Feed):
    name = 'huxiu'
    url = r'http://www.huxiu.com/rss/0.xml'
    capture = {}
    capture["catch"] = ['div.article-img-box','#article_content']
    capture["block_img"] = ['1024235475.jpg']

    def process_image(self, img):
        url = img['src'] if 'src' in img.attrs else None
        if not url: return
        for key_word in self.capture["block_img"]:
            if key_word in url: return img.decompose()
        url = url.split('?')[0]
        img['src'] = url.replace('bipush','huxiu')

recipe = Huxiu