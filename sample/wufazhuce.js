
const Base = require('../common/recipe/rank.js')
const cheerio = require('cheerio')

module.exports = class Feed extends Base{
  init(){
    let self = this
    super.init()
    this.name = 'ONE一个'
    this.url = 'http://wufazhuce.com/'
    this.capture.catch = ['.one-articulo']
    this.capture.remove = ['.articulo-compartir']
    this.rankCapture.flag = ($)=>{
      let title = $('.one-articulo-titulo>a')
      self.name = title.text().replace(/\s+/g, "")
      return self.name
    }
  }
  getRankList($){
    let title = $('.one-articulo-titulo>a')
    return [title.attr('href')]
  }
}
