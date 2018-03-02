
const Koa = require('koa')
const engine = require('./engine.js')
const route = require('./route.js')
const spider = require('./spider.js')
let AV = engine.AV

let app = new Koa()
app.use(AV.koa())
app = route(app)

AV.Cloud.define('spider', ()=>{
  spider.run().then(()=>{console.log('Auto spider done')}).catch((e)=>{console.error(e)})
  return true
})
AV.Cloud.define('clear', ()=>{
  spider.clear().then(()=>{console.log('Auto clear done')}).catch((e)=>{console.error(e)})
  return true
})
AV.Cloud.define('wakeup', ()=>{
  console.log('App is wake up now')
  return true
})

app.listen(engine.port)
