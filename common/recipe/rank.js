
// 定义了网页抓取相关的方法，专门用于将一个日榜类的网页转换为 RSS

const Base = require('./base.js')
const urlGet = require('../util/urlGet.js')
const cheerio = require('cheerio')

class Feed extends Base{
  init(){
    super.init()
    this.rankCapture = { size: null, catch: [], flag: ($)=>{ return null } }
  }
  getRankList($){
    let rankSpider = new Base(this.info)
    rankSpider.capture.nav = this.rankCapture.catch
    let [list] = rankSpider.spiderCheckNav($('body').html(), this.url)
    return list
  }
  getRankResult(result){
    return [{
      title: this.name, date: new Date(), link: this.url,
      content: result.join('')
    }]
  }
  async getFeed(){
    let self = this
    let lastCheck = this.getLastCheck()
    let pubDate = new Date(new Date(new Date().toLocaleDateString()).getTime())
    if (lastCheck > pubDate){
      console.log(`${this.name} has captured today`)
      return []
    }
    let html = await urlGet(this.url, {allowError: true, encode: this.encode})
    if (!html){ return [] }
    let $ = cheerio.load(html)
    let flag = this.rankCapture.flag($)
    if (this.getLastFlag() == flag){
      console.log(`${this.name} has no update after last spider`)
      return []
    }
    this.setLastCheck()
    this.setLastFlag(flag)
    let list = this.getRankList($)
    if (this.rankCapture.size && list.length > this.rankCapture.size){ list = list.slice(0, this.rankCapture.size) }
    let result = []
    list = list.map(async (url, i)=>{
      let content = await this.spiderMain(url, url)
      result[i] = this.generateHtml(content)
    })
    await Promise.all(list)
    if (result.length > 0){ return this.getRankResult(result) }
    return []
  }
}

module.exports = Feed
