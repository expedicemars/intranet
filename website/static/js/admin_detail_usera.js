import httpGet from "./httpGet.js"

let detail_usera = httpGet("/send_admin/detail_usera_"+document.getElementById("id").value)
document.getElementById("temp").innerHTML = detail_usera