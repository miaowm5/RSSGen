# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, urllib
from leancloud import Object, Query, LeanCloudError
import auth

Url = Object.extend('UrlList')

def save_data(data):
    try: data.save()
    except LeanCloudError, e: print e

def save(url, title):
    item = Url()
    url = urllib.unquote(url)
    title = urllib.unquote(title)
    item.set('url',url)
    item.set('title',title)
    save_data(item)

def get():
    query = Query(Url)
    query.descending("createdAt")
    result = []
    for e in query.find(): result.append([e.get('url'), e.get('title'), e.id])
    return result

def delete(id):
    query = Query(Url)
    try:
        e = query.get(id)
        e.destroy()
        return 'Url remove from list!'
    except LeanCloudError, e: return str(e)