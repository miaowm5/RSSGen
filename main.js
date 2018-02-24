
const Koa = require('koa')
const engine = require('./engine.js')
const route = require('./route.js')
const spider = require('./spider.js')
let AV = engine.AV

let app = new Koa()
app.use(AV.koa())
app = route(app)

AV.Cloud.define('spider', ()=>{ return spider.run() })
AV.Cloud.define('clear', ()=>{ return spider.clear() })

app.listen(engine.port)
