import httpGet from "./httpGet.js"
let role_uzivatele = JSON.parse(httpGet("/send_admin/role_" + parseInt(document.getElementById("id").value)))
let seznam_omezeni = JSON.parse(httpGet("/send_admin/vsechny_omezeni"))
console.log(role_uzivatele)
console.log(seznam_omezeni)