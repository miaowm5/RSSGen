
const Router = require('koa-router')
const router = new Router()
const qr = require('qr-image')
const spider = require('./spider.js')
const bookmark = require('./bookmark.js')
const tpl = (path, data)=>{
  const xtpl = require('xtpl')
  return new Promise((s,r)=>{
    xtpl.renderFile('./views/'+path+'.xtpl', data, (e,c)=>{ if (e){ r(e) }else{ s(c) } })
  })
}

router.get('/', async (ctx)=>{
  ctx.response.body = await tpl('index', {})
})
router.get('/qr', (ctx)=>{
  let query = ctx.request.query
  if (query.url){
    ctx.response.type = 'image/png'
    let url = encodeURIComponent(query.url)
    let title = encodeURIComponent(query.title||'')
    ctx.response.body = qr.imageSync(`${ctx.protocol}://${ctx.host}/bookmark?type=url&url=${url}&title=${title}`)
  }
})
router.get('/rss', async (ctx)=>{
  let query = ctx.request.query
  let list = await spider.getList()
  if (query.type == 'save'){
    if (list.includes(query.recipe)){
      spider.run(query.recipe)
      ctx.response.body = 'Spider start...'
      return
    }
  }
  if (query.type == 'saveall'){
    spider.run(); ctx.response.body = 'Spider start...'
    return
  }
  if (query.type == 'clearall'){
    spider.clear(); ctx.response.body = 'Clear start...'
    return
  }
  list = list.map((key)=>{
    let data = require('./recipe/'+key)
    data = new data()
    return [key, data.name]
  })
  ctx.response.body = await tpl('rss', {list})
})
router.get('/rss/:title', async (ctx)=>{
  ctx.response.type = 'text/xml'
  ctx.response.body = await spider.show(ctx.params.title, `${ctx.protocol}://${ctx.host}`)
})
router.get('/bookmark', async (ctx)=>{
  let query = ctx.request.query
  if (query.type == 'add'){ if (query.url){
    await bookmark.add(query.url, query.title)
    ctx.response.body = 'Save bookmark...'
    return
  }}
  else if (query.type == 'del'){ if (query.id){
    await bookmark.del(query.id)
    ctx.response.body = 'Delete bookmark...'
    return
  }}
  else if (query.type == 'url'){ if (query.url){
    ctx.response.body = await tpl('bookmark',
      {type:'url', title: query.title || 'Untitled', url: query.url})
    return
  }}
  let list = await bookmark.get()
  ctx.response.body = await tpl('bookmark', {type:'list', list})
})

module.exports = (app)=>{
  app.use(router.routes())
  app.use(require('koa-static')(__dirname+'/static'))
  return app
}
