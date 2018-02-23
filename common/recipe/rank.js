
// 定义了网页抓取相关的方法，专门用于将一个排行榜类的网页转换为 RSS

const Base = require('./base.js')
const urlGet = require('../util/urlGet.js')

class Feed extends Base{
  init(){
    super.init()
    this.rankCapture = {size: null, catch: []}
  }
  async getFeed(){
    let self = this
    let lastCheck = this.getLastCheck()
    let pubDate = new Date(new Date(new Date().toLocaleDateString()).getTime())
    if (lastCheck > pubDate){
      console.log(`${this.name} has captured today`)
      return []
    }
    let rank = await urlGet(this.url, {allowError: true})
    if (!rank){ return [] }
    this.setLastCheck()
    let rankSpider = new Base(this.info)
    rankSpider.capture.nav = this.rankCapture.catch
    let [list] = rankSpider.spiderCheckNav(rank, this.url)

    if (this.rankCapture.size && list.length > this.rankCapture.size){ list = list.slice(0, this.rankCapture.size) }
    let result = []
    list = list.map(async (url, i)=>{
      let content = await this.spiderMain(url, url)
      result[i] = this.generateHtml(content)
    })
    await Promise.all(list)
    if (result.length > 0){
      return [{
        title: this.name, date: pubDate, link: this.url,
        content: result.join('')
      }]
    }
    return []
  }
}

module.exports = Feed
