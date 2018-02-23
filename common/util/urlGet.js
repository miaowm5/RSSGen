
const r2 = require('r2')

const get = async (url, opt={})=>{
  opt = Object.assign({
    allowError: false
  },opt)
  let headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
  try{
    let r = await r2(url, {headers}).response
    if (r.status == 200){ return r.text() }
    console.error(`HTTP error code: ${r.status}`)
    throw `HTTP error code: ${r.status}`
  }catch(e){
    console.error(`Unable to get url:${url}`)
    if (opt.allowError){ return null }
    else{ throw(e) }
  }
}

module.exports = get
