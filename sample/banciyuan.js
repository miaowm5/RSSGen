
const Base = require('../common/recipe/rank.js')

module.exports = class Feed extends Base{
  init(){
    super.init()
    this.name = '半次元日榜'
    this.url = 'http://bcy.net/illust/toppost100?type=lastday'
    this.rankCapture.size = 10
    this.rankCapture.catch = ['.js-workTopList ._box>a']
    this.capture.catch = ['.post__title','.w650']
  }
  processImg($, e, url){
    let src = $(e).attr('src')
    if (src) $(e).attr('src', src.replace("/w650", ''))
    return super.processImg($, e, url)
  }
}
