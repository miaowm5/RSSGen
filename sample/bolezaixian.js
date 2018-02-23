
const Base = require('../common/recipe/feed2.js')

module.exports = class Feed extends Base{
  init(){
    super.init()
    this.name = '伯乐在线Web'
    this.url = 'http://web.jobbole.com/feed/'
    this.capture.catch = ['.entry']
    this.capture.remove = ['.copyright-area','#single-page-inner-widget','.post-adds','#author-bio','.crayon-main']
  }
}
