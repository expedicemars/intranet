import httpGet from "./httpGet.js"

let data = JSON.parse(httpGet("/send_admin/data_pro_motivaky_a_prace"))
console.log(data)