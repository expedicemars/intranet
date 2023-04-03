import httpGet from "./httpGet.js"
let datum = httpGet("noauth_api/registrace_pretty")
document.getElementById("date").innerHTML = datum
