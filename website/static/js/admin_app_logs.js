import httpGet from "./httpGet.js"

document.getElementById("logs").innerHTML = JSON.parse(httpGet("/send_admin/app_logs"))
