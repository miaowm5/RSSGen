# !/usr/bin/env python
# -*- coding:utf-8 -*-

from base import Base, UTC
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class Feed(Base):

    name = 'wufazhuce'
    url = r'http://wufazhuce.com/'
    oldest = 7
    capture = {}
    capture["catch"] = ['.one-articulo']
    capture["remove"] = ['.articulo-compartir']

    def get_item(self):
        # yield title, time, link, content
        content = self.featch_content(self.url)
        if not content: return
        last_check = self.get_last_check()
        soup = BeautifulSoup(content,'lxml')
        last_update = soup.select('p.one-titulo')[0].get_text().strip().replace('VOL.','')
        last_update = datetime(2012,10,7,tzinfo=UTC(0)) + timedelta(days=int(last_update))
        if last_check >= last_update:
            print '%s has no update after last spider' % self.name
            return
        adom = soup.select('.one-articulo-titulo a')[0]
        url = adom['href']
        content = self.featch_content(url)
        if not content: return
        content = self.process_article(content)
        content = unicode(content.body)
        title = adom.get_text(strip=True).encode('utf-8')
        yield title, last_update, url, content
        self.refresh_last_check(last_update)

recipe = Feed