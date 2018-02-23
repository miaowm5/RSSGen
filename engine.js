
const AV = require('leanengine')

let config
try{
  const fs = require('fs')
  if (!fs.existsSync('./config.json')) throw 'Use system config.'
  config = JSON.parse(fs.readFileSync('./config.json').toString())
}
catch(e){
  config = {
    appId: process.env.LEANCLOUD_APP_ID,
    appKey: process.env.LEANCLOUD_APP_KEY,
    masterKey: process.env.LEANCLOUD_APP_MASTER_KEY,
    port: process.env.LEANCLOUD_APP_PORT
  }
}

AV.init(config)
let Data = {}
let databaseName = ["Log", "FeedInfo", "FeedItem", "Bookmark", "AppInfo"]
databaseName.forEach((key)=>{ Data[key] = AV.Object.extend(key) })

module.exports = { AV, Data, port: config.port }
