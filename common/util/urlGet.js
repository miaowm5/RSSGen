
const request = require('superagent')
const charset = require('superagent-charset')
charset(request)

const get = async (url, opt={})=>{
  opt = Object.assign({
    allowError: false,
    encode: null,
  },opt)
  let r = request.get(url)
    .set('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    .buffer(true)
  if (opt.encode){ r.charset(opt.encode) }
  try{
    let res = await r
    if (res.status == 200){ return res.text }
    console.error(`HTTP error code: ${res.status}`)
    throw `HTTP error code: ${res.status}`
  }catch(e){
    console.error(`Unable to get url:${url}`)
    if (opt.allowError){ return null }
    else{ throw(e) }
  }
}

module.exports = get
