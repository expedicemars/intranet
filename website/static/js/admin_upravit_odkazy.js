import httpGet from "./httpGet.js"

let odkazy = JSON.parse(httpGet("/admin_api/odkazy"))
let content_div = document.getElementById("content")

for (let i = 0; i<odkazy.length;i++) {
    let o = odkazy[i]
    let row = document.createElement("div")
    row.classList.add("row")
    content_div.appendChild(row)
    let col1 = document.createElement("div")
    col1.classList.add("col-7")
    row.appendChild(col1)
    let col2 = document.createElement("div")
    col2.classList.add("col-3")
    row.appendChild(col2)
    let a = document.createElement("a")
    a.href = o["odkaz"]
    a.innerHTML = o["popis"]
    a.target="_blank"
    a.classList.add("link")
    col1.appendChild(a)
    let button = document.createElement("button")
    button.classList.add("btn", "btn-danger")
    button.type="submit"
    button.innerHTML = "Smazat"
    button.name = "smazat"
    button.value = i
    content_div.appendChild(document.createElement("br"))
    col2.appendChild(button)
}