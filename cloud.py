# !/usr/bin/env python
# -*- coding:utf-8 -*-

import spider

def spider_work():
    print('spider start')
    spider.save()
    print('spider over')

def clear_old_feed():
    print('clear start')
    spider.clear()
    print('clear over')
