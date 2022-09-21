import httpGet from "./httpGet.js"
let exporty = JSON.parse(httpGet("/send_admin/exporty"))
let content_div = document.getElementById("content")

function generator(isoformat ,pretty, filename) {
    let row = document.createElement("div")
    row.classList.add("row", "my-1")
    content_div.appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col")
    row.appendChild(col1)

    let a = document.createElement("a")
    a.innerHTML = pretty
    a.download = filename
    a.href = "/send_zip/" + filename
    col1.appendChild(a)

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)

    let btn = document.createElement("button")
    btn.classList.add("btn", "btn-danger")
    btn.innerHTML = "Smazat export"
    btn.type = "submit"
    btn.name = "smazat"
    btn.value = isoformat
    col2.appendChild(btn)
}

for (let zaznam of exporty) {
    generator(zaznam["iso"], zaznam["datum"], zaznam["filename"])
}