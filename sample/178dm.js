
const Base = require('../common/recipe/feed.js')

module.exports = class Feed extends Base{
  init(){
    super.init()
    this.name = '178动漫'
    this.url = 'http://acg.178.com/s/rss.xml'
    this.capture.blockImg = ['159502145898']
    this.capture.oldest = 1
  }
}
