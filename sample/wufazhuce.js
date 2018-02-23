
const Base = require('../common/recipe/base.js')
const cheerio = require('cheerio')
const urlGet = require('../common/util/urlGet.js')

module.exports = class Feed extends Base{
  init(){
    super.init()
    this.name = 'ONE一个'
    this.url = 'http://wufazhuce.com/'
    this.capture.catch = ['.one-articulo']
    this.capture.remove = ['.articulo-compartir']
  }
  async getFeed(){
    let lastCheck = this.getLastCheck()
    let pubDate = new Date(new Date(new Date().toLocaleDateString()).getTime())
    if (lastCheck > pubDate){
      console.log(`${this.name} has captured today`)
      return []
    }
    let html = await urlGet(this.url, {allowError: true})
    if (!html) return []
    let $ = cheerio.load(html)
    let title = $('.one-articulo-titulo>a')
    let link = title.attr('href')
    let content = await this.spiderMain(link)
    this.setLastCheck()
    return [{title: title.text().replace(/\s+/g, ""), date: pubDate, link, content: this.generateHtml(content)}]
  }
}
