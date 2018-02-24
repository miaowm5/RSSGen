
const {AV, Data} = require('./engine.js')

class Bookmark{
  async get(){
    let list = (new AV.Query('Bookmark')).descending("createdAt")
    list = await list.find()
    return list.map((u)=>{ return [u.get('url'), u.get('title'), u.id] })
  }
  async del(id){
    let item = await (new AV.Query('Bookmark')).get(id)
    if (item){ await item.destroy() }
  }
  async add(url, title){
    let item = new Data['Bookmark']()
    item.set('url', decodeURI(url))
    item.set('title', decodeURI(title || 'Untitle'))
    await item.save()
  }
}

module.exports = new Bookmark()
