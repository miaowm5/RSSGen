
// 定义了 Feed 需要的相关方法，用于将其他网站的全文 RSS 转存到服务器上

const Base = require('./base.js')
const Parser = require('rss-parser')
const urlGet = require('../util/urlGet.js')

class Feed extends Base{
  async parseFeed(feed){
    let title = feed.title
    let link = feed.link
    let content = feed.content || feed['content:encoded'] || ''
    return {title, link, content}
  }
  async getFeed(){
    let rss = await urlGet(this.url, {allowError: true, encode: this.encode})
    if (!rss){ return [] }
    try{
      let parser = new Parser()
      rss = await parser.parseString(rss) }
    catch(e){
      console.error(e)
      return []
    }
    let lastCheck = this.getLastCheck()
    if (rss.pubDate){
      if (lastCheck > new Date(rss.pubDate)){ return [] }
    }
    this.setLastCheck()
    let result = []
    for (let feed of rss.items){
      let feedDate = new Date(feed.pubDate)
      if (feed.pubDate){ if (lastCheck > feedDate){ break } }
      let r = await this.parseFeed(feed)
      if (r){
        r.date = feedDate
        result.push(r)
      }
    }
    return result
  }
}

module.exports = Feed
