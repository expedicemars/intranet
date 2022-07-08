import httpGet from "./httpGet.js"
let datum = JSON.parse(httpGet("send_noauth/registrace"))
let d = new Date(datum["date"])
document.getElementById("date").innerHTML = d.toLocaleDateString()
