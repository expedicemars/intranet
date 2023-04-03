import httpGet from "./httpGet.js"

let contentdiv = document.getElementById("content")
let progressy = JSON.parse(httpGet("/admin_api/vsechny_progressy"))
let informace = JSON.parse(httpGet("/admin_api/vsechny_informace"))

for (let p of progressy) {
    contentdiv.appendChild(document.createElement("hr"))
    let h3 = document.createElement("h3")
    h3.innerText = p
    contentdiv.appendChild(h3)
    let textarea = document.createElement("textarea")
    textarea.classList.add("form-control")
    textarea.name = p
    textarea.id = p
    contentdiv.appendChild(textarea)
}

progressy.push("Obecné")
for (let i of informace) {
    document.getElementById(i["nadpis"]).innerText = i["content"]
}