import httpGet from "./httpGet.js"
let emaily = httpGet("/send_admin/emaily_admin_editoru")
let mailing_list = httpGet("/send_admin/mailing_list")

document.getElementById("emails").innerHTML = emaily
document.getElementById("mailing_list").innerHTML = JSON.parse(mailing_list)