
const Router = require('koa-router')
const router = new Router()
const qr = require('qr-image')
const spider = require('./spider.js')
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
    ctx.response.body = qr.imageSync(decodeURI(query.url))
  }
})
router.get('/rss', async (ctx)=>{
  let query = ctx.request.query
  let list = await spider.getList()
  if (query.type == 'save'){
    if (list.includes(query.recipe)){
      spider.run(query.recipe)
      ctx.response.body = '正在后台更新中...'
      return
    }
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

module.exports = (app)=>{
  app.use(router.routes())
  app.use(require('koa-static')(__dirname+'/static'))
  return app
}
