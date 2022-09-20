import httpGet from "./httpGet.js"
let pohovory = JSON.parse(httpGet("/send_user/pohovory"))
let aktualne_div = document.getElementById("aktualne")
let pohovory_div = document.getElementById("pohovory")

function generator(iso, pretty) {
    let row = document.createElement("div")
    row.classList.add("row")
    let col1 = document.createElement("div")
    col1.classList.add("col")
    let col2 = document.createElement("div")
    col2.classList.add("col")
    let zapsat_button = document.createElement("button")
    zapsat_button.innerHTML = "Zapsat tenhle termín"
    zapsat_button.classList.add("btn", "btn-primary", "my-1")
    zapsat_button.type="submit"
    zapsat_button.name = "smazat"
    zapsat_button.value = iso

    col1.innerHTML = pretty
    col2.appendChild(zapsat_button)
    row.appendChild(col1)
    row.appendChild(col2)
    pohovory_div.appendChild(row)
}

for (let p of pohovory) {
    generator(p["iso"], p["pretty"])
}