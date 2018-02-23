
// 定义了 Feed 需要的相关方法，用于将非全文 RSS 转为全文 RSS

const Base = require('./feed.js')
const Parser = require('rss-parser')

class Feed extends Base{
  async parseFeed(feed){
    let result = await super.parseFeed(feed)
    let content = feed.link
    content = await this.spiderMain(content, content)
    content = this.generateHtml(content)
    result.content = content
    return result
  }
}

module.exports = Feed
