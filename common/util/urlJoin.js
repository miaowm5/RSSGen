
const {URL} = require('url')

module.exports = (base, href)=>{
  const url = new URL(href, base)
  return url.toString()
}
