
// 最为基础的抓取类，定义了所有 recipe 的通用方法
const cheerio = require('cheerio')
const he = require('he')
const urlGet = require('../util/urlGet.js')
const urlJoin = require('../util/urlJoin.js')
const defaultInfo = { get: ()=>null, set: ()=>null }

class Base{
  constructor(info){
    this.info = info || defaultInfo
    this.log = []
    this.init()
  }
  init(){
    this.name = 'Feed Name'
    this.url = 'Detect URL'
    this.capture = {
      catch: [], remove: [],
      nav: [], blockImg: [], oldest: 2
    }
  }
  addLog(type, ...info){ this.log.push({type, info}) }
  process(html, url){
    let self = this
    let $ = cheerio.load(html)
    const wrap = (e)=>{
      e.parent().append(`<div>${e.html()}</div>`)
      e.remove()
    }
    $('body').contents().each((i,e)=>{ if (e.type == 'comment'){ $(e).remove() } })
    if (self.capture.catch.length > 0){
      let html = '<body>'
      self.capture.catch.forEach((c)=>{ html += $.html(c) })
      html += '</body>'
      $ = cheerio.load(html)
    }
    let div = ['script','object','video','embed','noscript','style','link']
    div = div.concat(this.capture.remove)
    div.forEach(function(d){ $(d).each(function(i, e){ $(this).remove() }) })
    div = ['article', 'aside', 'header', 'footer', 'nav', 'figcaption', 'figure', 'section', 'time']
    div.forEach((d)=>{ $(d).each(function(i, e){ wrap($(this), 'div') }) })
    $('textarea').each(function(i, e){ wrap($(this), 'pre') })
    $('img').each(function(i, e){ self.processImg($, e, url) })

    let attrs = ['width','height','onerror','onclick','onload','style','id','class',
      'title','alt','align','border','itemprop','name']
    $('*').each((i,e)=>{ attrs.forEach((attr)=>{ $(e).removeAttr(attr) }) })
    return he.decode($('body').html()).replace(/[\n]/ig,'')
  }
  processImg($, e, url){
    let src = $(e).attr('src')
    if (!src){ $(e).remove(); return }
    $(e).attr('src', urlJoin(url, src))
    if (this.capture.blockImg.length == 0) return
    let block = this.capture.blockImg.find((url)=>{ return src.includes(url) })
    if (block){ $(e).remove() }
  }
  getLastCheck(){
    let oldest = new Date()
    oldest.setDate(oldest.getDate()-this.capture.oldest)
    let lastCheck = this.info.get('lastCheck')
    if (!lastCheck) return oldest
    if (lastCheck > oldest) return lastCheck
    return oldest
  }
  setLastCheck(time=null){
    if (!time) time = new Date()
    this.info.set('lastCheck', time)
  }
  spiderCheckNav(html, detectUrl){
    if (!html) return [[], null]
    if (this.capture.nav.length == 0) return [[], null]
    const $ = cheerio.load(html)
    let urlList = []
    this.capture.nav.forEach((nav)=>{
      $(nav).each(function(i, e){
        let href = $(this).attr('href')
        if (!href) return
        href = urlJoin(detectUrl, href)
        if (href == detectUrl) return
        urlList.push(href)
      })
    })
    return [urlList, null]
  }
  generateHtml(result){
    let self = this
    let content = ''
    result.forEach((value)=>{
      if (!value.html) return
      try{ content += self.process(value.html, value.url) }
      catch(e){
        console.error(e)
        self.addLog('fail_process', value.url, value.html, e)
        content += `<p>*** This Page Generate Fail ***</p><a href="${value.url}">Source Link</a>`
      }
    })
    return content
  }
  async spiderMain(capture=[], detect = null){
    let self = this
    let result = []
    let cache = {}
    let refreshTask = (capture, detect)=>{
      if (!capture) capture = []
      if (!Array.isArray(capture)){ capture = [capture] }
      let task = capture
      if (detect){ task = task.concat(detect) }
      task = task.filter((v)=>{return cache[v] === undefined})
      task = Array.from(new Set(task))
      return task
    }
    let task = refreshTask(capture, detect)
    while (task.length > 0){
      let promise = task.map((url)=>{ return urlGet(url, {allowError: true}) })
      promise = Promise.all(promise)
      let page = await promise
      page.forEach((html,i)=>{
        let url = task[i]
        cache[url] = html
        if (html){ if (capture.includes(url)){ result.push({url, html}) } }
        else{ console.log(`Fetch URL failed, skip(${url})`) }
      })
      task = []
      if (detect){
        [capture, detect] = self.spiderCheckNav(cache[detect], detect)
        task = refreshTask(capture, detect)
      }
    }
    return result
  }
  async getFeed(){
    let title = 'Sample feed title'
    let date = new Date()
    let link = 'http://www.miaowm5.com'
    let content = 'Sample feed content'
    let feed = {title, date, link, content}
    let feeds = [feed]
    this.setLastCheck()
    return feeds
  }
}

module.exports = Base
