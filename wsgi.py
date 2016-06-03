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
    orss = spider.online_rss_list()
    return bottle.template('rss_list', rss=rss, orss=orss)

@app.route('/rss/<name>')
def show_rss(name):
    return spider.show(name)

@app.route('/rss/save')
def save_rss():
    recipe = bottle.request.query.recipe
    if bottle.request.query.type == 'rss': spider.save(all_feed=True, feed_name=recipe)
    else: spider.save_online(feed_name="ol-%s" % recipe)
    return 'save over'

@app.post('/rss/delete')
def delete_rss():
    spider.remove_online_feed(feed_name=bottle.request.params.recipe)

@app.route('/list')
def show_list():
    return bottle.template('list', items=lists.get())

@app.route('/list/save')
def add_list():
    url = bottle.request.query.url
    title = bottle.request.query.title
    lists.save(url, title)
    return 'Url add to list!'

@app.post('/list/delete')
def delete_list():
    lists.delete(bottle.request.params.id)

application = leancloud.Engine(app)

@application.define
def spider_work(): cloud.spider_work()

@application.define
def clear_old_feed(): cloud.clear_old_feed()

@app.route('/test/work')
def test_work():
    return cloud.spider_work()