import httpGet from "./httpGet.js"
let datum = httpGet("send_noauth/registrace_pretty")
document.getElementById("date").innerHTML = datum
