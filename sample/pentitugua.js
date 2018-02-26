
const Base = require('../common/recipe/rank.js')
const cheerio = require('cheerio')

module.exports = class Feed extends Base{
  init(){
    let self = this
    super.init()
    this.name = '喷嚏图卦'
    this.encode = 'gbk'
    this.url = 'http://www.dapenti.com/blog/blog.asp?subjectid=70&name=xilei'
    this.rankCapture.catch = ['.oblog_t_2 ul>li:nth-child(1)>a']
    this.rankCapture.size = 1
    this.capture.catch = ['div.oblog_text']
    this.rankCapture.flag = ($)=>{
      let title = $('.oblog_t_2 ul>li:nth-child(1)>a').text()
      self.name = title
      return self.name
    }
  }
}
