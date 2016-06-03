# !/usr/bin/env python
# -*- coding:utf-8 -*-

import spider

def spider_work():
    print('spider start')
    spider.save()
    spider.save_online()
    print('spider over')

def clear_old_feed():
    print('clear start')
    spider.clear()
    spider.clear_online()
    print('clear over')
