import httpGet from "./httpGet.js"

let detail_usera = JSON.parse(httpGet("/send_admin/detail_usera_"+document.getElementById("id").value))
document.getElementById("temp").innerHTML = JSON.stringify(detail_usera, null, 4)