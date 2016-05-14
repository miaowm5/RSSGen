# !/usr/bin/env python
# -*- coding:utf-8 -*-

import leancloud, auth
from lib import bottle
import spider, lists, cloud

app = bottle.Bottle()

@app.route('/')
def Home():
    return 'It Works!'

@app.route('/static/<filename>')
def static(filename):
    return bottle.static_file(filename, root='./static')

@app.route('/rss')
def show_rss_list():
    rss = [a.name for a in spider.rss_list()]
    return bottle.template('rss_list', rss=rss)

@app.route('/rss/<name>')
def show_rss(name):
    return spider.show(name)

@app.route('/list')
def show_list():
    return bottle.template('list', items=lists.get())

@app.route('/list/save')
def add_list():
    url = bottle.request.query.url
    title = bottle.request.query.title
    lists.save(url, title)
    return 'Url add to list!'

@app.route('/list/delete')
def delete_list():
    return lists.delete(bottle.request.query.id)

application = leancloud.Engine(app)

@application.define
def spider_work(): cloud.spider_work()

@application.define
def clear_old_feed(): cloud.clear_old_feed()

@app.route('/test/work')
def test_work():
    return cloud.spider_work()

@app.route('/test/work/<recipe>')
def test_work(recipe):
    return spider.save(recipe)
