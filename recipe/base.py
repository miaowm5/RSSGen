# !/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib, urllib2
from datetime import datetime, timedelta, tzinfo
from bs4 import BeautifulSoup, Comment

class UTC(tzinfo):
    def __init__(self,offset = 0): self._offset = offset
    def utcoffset(self, dt): return timedelta(hours=self._offset)
    def tzname(self, dt): return "UTC +%s" % self._offset
    def dst(self, dt): return timedelta(hours=self._offset)

class Base(object):

    name = 'Feed Name'
    url = 'Detect URL'
    capture = {}
    capture["catch"] = []
    capture["remove"] = []
    capture["nav"] = ''
    oldest = 2

    def __init__(self, info):
        self.info = info
        default_capture = {}
        default_capture["catch"] = []
        default_capture["remove"] = []
        default_capture["nav"] = ''
        default_capture.update(self.capture)
        self.capture = default_capture

    def featch_url(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        try:
            result = urllib2.urlopen(urllib2.Request(url=url,headers=headers))
            if result.getcode() == 200: return result.read()
            else: error = result.getcode()
        except Exception as e: error = str(e)
        print('Featch URL Fail(%s): %s' % (url, error))
        return None

    def featch_content(self, url):
        content = self.featch_url(url)
        return content

    def spider_main(self, detect = None, capture = set()):
        detect  = detect
        capture = capture
        done    = set()
        cache   = {}
        result  = []
        task = capture if detect is None else (set([detect]) | capture)
        task = task - done
        while len(task) > 0:
            for url in task:
                cache[url] = None
                content = self.featch_content(url)
                if content: cache[url] = content
                else: print('Fetch URL failed, skip(%s)' % url)
            for url in capture:
                if not url in done: result.append( (cache.get(url, None), url) )
            spider = self.spider_refresh_capture(detect, cache.get(detect, None))
            if len(spider) >= 3:
                if spider[2]: result.append( (cache.get(detect, None), detect) )
            detect, capture = spider[0], spider[1]
            done.add(url)
            cache = {}
            task = capture if detect is None else (set([detect]) | capture)
            task = task - done
        return result

    def spider_refresh_capture(self, url, html):
        # return detect_url, set([capture_url])[, add_detect_to_result]
        if html is None: return None, set()
        capture = set()
        if self.capture.get('nav', None):
            soup = BeautifulSoup(html, "lxml")
            nav = soup.select(self.capture["nav"])
            for e in nav:
                page_url = e["href"]
                if (page_url != url): capture.add(page_url)
        return None, capture

    def spider_generate_html(self, result):
        content = u''
        for html, url in result:
            try:
                if not html: continue
                soup = self.process_article(html)
                content += unicode(soup.html.body.next)
            except Exception as e:
                print('Creat html fail(%s):%s' % (url, str(e)))
                content += '<p>*** This Page Get Fail ***</p><a href="%s">Link</a>' % url
        return content

    def convert_time(self, time):
        return datetime(*(time[0:6]),tzinfo=UTC(0))

    def get_last_check(self):
        oldest_days = datetime.utcnow() - timedelta(days=self.oldest)
        oldest_days = self.convert_time(oldest_days.timetuple())
        last_check = self.info.get('check')
        if last_check is None: return oldest_days
        if last_check > oldest_days: return last_check
        else: return oldest_days

    def refresh_last_check(self, time):
        self.info.set('check', time)

    def process_article(self, content):
        if isinstance(content,(str)): soup = BeautifulSoup(content,'lxml')
        else: soup = content
        if self.capture["catch"]:
            body = soup.new_tag('body')
            for spec in self.capture["catch"]:
                tags = [tag for tag in soup.select(spec)]
                for tag in tags: body.append(tag)
            soup.find('body').replace_with(body)
        remove = ['script','object','video',
            'embed','noscript','style','link','#controlbar_container']
        remove += self.capture["remove"]
        for spec in remove:
            tags = [tag for tag in soup.select(spec)]
            for tag in tags: tag.decompose()
        remove_attrs = ['width','height','onerror','onclick','onload','style','id','class',
            'title','alt','align']
        for attr in remove_attrs:
            for tag in soup.find_all(attrs={attr:True}): del tag[attr]
        for cmt in soup.find_all(text=lambda text:isinstance(text, Comment)):
            cmt.extract()
        for x in soup.find_all(['article', 'aside', 'header', 'footer', 'nav',
            'figcaption', 'figure', 'section', 'time']):
            x.name = 'div'
        for x in soup.find_all(['textarea']): x.name = 'pre'
        return soup

    def get_item(self):
        # yield title, time, link, content
        pass
