
const fs = require('fs')
const {AV, Data} = require('./engine.js')

const createDatabase = async ()=>{
  let createDatabase = async (database)=>{
    console.log(`Create Database: ${database}`)
    let query = new AV.Query(database)
    try{ await query.find() }
    catch(e){
      let item = new Data[database]()
      item = await item.save()
      item = AV.Object.createWithoutData(database, item.id)
      await item.destroy()
    }
  }
  let database = Object.keys(Data).map(createDatabase)
  database = Promise.all(database)
  await database
}
const checkRecipe = async ()=>{
  let list = fs.readdirSync('./recipe')
  let recipeList = []
  list.forEach((file)=>{
    if (!file.endsWith('.js')) return
    recipeList.push(file)
  })
  let query = new AV.Query('AppInfo')
  let appInfo = await query.first()
  if (!appInfo){ appInfo = new Data['AppInfo']() }
  appInfo.set('recipeList',recipeList)
  await appInfo.save()

  query = new AV.Query('FeedInfo').notContainedIn('name', recipeList)
  query = await query.find()
  await AV.Object.destroyAll(query)
  query = new AV.Query('FeedItem').notContainedIn('name', recipeList)
  query = await query.find()
  await AV.Object.destroyAll(query)
}

const init = async ()=>{
  await createDatabase()
  await checkRecipe()
}

console.log('Init database')
init()
  .then((r)=>{ console.log(`Init over`) })
  .catch((e)=>{ console.error(e) })
