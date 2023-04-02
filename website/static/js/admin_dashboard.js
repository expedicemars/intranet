import httpGet from "./httpGet.js"
let emaily = httpGet("/send_admin/emaily_admin_editoru")
let odkazy = JSON.parse(httpGet("/send_admin/odkazy"))
let odkazy_list = document.getElementById("odkazy")

document.getElementById("emails").innerHTML = emaily
document.getElementById("datum_konce_registrace").innerHTML = httpGet("/send_noauth/registrace_pretty")

for (let o of odkazy) {
    let li = document.createElement("li")
    odkazy_list.appendChild(li)
    let a = document.createElement("a")
    li.appendChild(a)
    a.innerHTML = o["popis"]
    a.href = o["odkaz"]
    a.target = "_blank"
}