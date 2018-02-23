
const {AV, Data} = require('./engine.js')

class Spider{
  async getList(){
    let appInfo = await (new AV.Query('AppInfo')).first()
    let list = appInfo.get('recipeList')
    return list
  }
  async getInfo(name){
    let self = this
    let query = (new AV.Query('FeedInfo')).equalTo('name', name)
    let info = null
    try{
      info = await query.first()
      if (!info) throw 'Info undefined'
    }catch(e){
      info = new Data['FeedInfo']()
      info.set('name', name)
      await self.save(info)
    }
    return info
  }
  async save(item){
    try{ await item.save() }
    catch(e){
      console.error(`Meet error when save item`)
      console.error(e)
    }
  }
  async run(name=null){
    console.log('Spider start')
    let self = this
    let list = [name]
    if (!name){ list = await this.getList() }
    list = list.map(async (name)=>{
      let info = await self.getInfo(name)
      let recipe = require('./recipe/'+name)
      recipe = new recipe(info)
      let feed
      try{ feed = await recipe.getFeed() }
      catch(e){
        console.error(`Get feed ${name} fail`)
        console.error(e)
        feed = []
      }
      if (feed.length > 0){
        feed = feed.map(async (feed)=>{
          let item = new Data['FeedItem']()
          item.set('name', name)
          item.set('title', feed.title)
          item.set('time', feed.date)
          item.set('link', feed.link)
          item.set('content', feed.content)
          await self.save(item)
        })
        await Promise.all(feed)
        await self.save(info)
        console.log(`Spider ${name}, find ${feed.length} new feed`)
      }
      let log = recipe.log.map(async (log)=>{
        let item = new Data['Log']()
        item.set('name', name)
        item.set('type', log.type)
        item.set('info', log.info)
        self.save(item)
      })
      await Promise.all(log)
    })
    await Promise.all(list)
    console.log('Spider over')
  }
  async clear(){
    console.log('clear old data')
    const feed = async ()=>{
      let list = await this.getList()
      list = list.map(async (name)=>{
        let recipe = require('./recipe/'+name)
        recipe = new recipe()
        let oldest = new Date()
        oldest.setDate(oldest.getDate()-recipe.capture.oldest)
        let feed = (new AV.Query('FeedItem')).equalTo('name', name).lessThan("time", oldest)
        feed = await feed.find()
        await AV.Object.destroyAll(feed)
        if (feed.length > 0) console.log(`${recipe.name} delete ${feed.length} old feed`)
      })
      await Promise.all(list)
    }
    const log = async ()=>{
      let oldest = new Date()
      oldest.setDate(oldest.getDate()-3)
      let log = (new AV.Query('Log')).lessThan("time", oldest)
      log = await log.find()
      await AV.Object.destroyAll(log)
    }
    await Promise.all([feed(), log()])
    console.log('clear over')
  }
  async show(name, url){
    const Feed = require('feed')
    let feed = new Feed({
      title: name, description: name, link: url,
      updated: new Date(), generator: 'RSSGen'
    })
    let item = (new AV.Query('FeedItem')).equalTo('name', name).descending('time')
    item = await item.find()
    item.forEach((item)=>{
      let link = item.get('link')
      let content = item.get('content')
      content += `<img src="${url}/qr?url=${encodeURI(link)}"></img>`
      feed.addItem({
        title: item.get('title'),
        link, content, description: content,
        date: item.get('time'),
      })
    })
    let result = feed.rss2()
    return result.replace('<rss version="2.0"',
      '<?xml-stylesheet type="text/xsl" href="../style/rss.xsl" ?><rss version="2.0"')
  }
}

module.exports = new Spider()

const testSpider = ()=>{
  try{
    let s = new Spider()
    s.run().then((r)=>console.log(r))
  }catch(e){
    console.error(e)
  }
}

// testSpider()

