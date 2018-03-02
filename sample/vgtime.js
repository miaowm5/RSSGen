
const Base = require('../common/recipe/feed.js')

module.exports = class Feed extends Base{
  init(){
    super.init()
    this.name = '游戏时光'
    this.url = 'http://www.vgtime.com/rss.jhtml'
    let self = this
    this.feedCapture.timeCorrect = false
    this.feedCapture.flag = (feed, t, f)=>{
      if (feed.title == f) return true
      self.flagToAdd.push(feed.title)
      return false
    }
    this.flagToAdd = []
  }
  async getFeed(){
    let result = await super.getFeed()
    this.setLastFlag(this.flagToAdd[0])
    return result
  }
}
