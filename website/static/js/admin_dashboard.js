import httpGet from "./httpGet.js"
let emaily = httpGet("/send_admin/emaily_admin_editoru")
document.getElementById("emails").innerHTML = emaily