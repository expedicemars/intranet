import httpGet from "./httpGet.js"
let pohovory = JSON.parse(httpGet("/send_user/volne_pohovory"))
let aktualne = JSON.parse(httpGet("/send_user/datum_pohovoru"))
let aktualne_div = document.getElementById("aktualne")
let pohovory_div = document.getElementById("pohovory")

if (aktualne["datum"]) {
    aktualne_div.innerHTML = "Momentálně máš vybrané tohle datum: " + aktualne["datum"]
} else {
    aktualne_div.innerHTML = "Momentálně nemáš vybrané žádné datum pohovoru."
}


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
    zapsat_button.name = "vybrat"
    zapsat_button.value = iso

    col1.innerHTML = pretty
    col2.appendChild(zapsat_button)
    row.appendChild(col1)
    row.appendChild(col2)
    pohovory_div.appendChild(row)
}

if (pohovory.length == 0) {
    pohovory_div.innerHTML = "Nejsou vypsané žádné termíny pohovorů."
} else {
    let p = document.createElement("p")
    p.innerHTML = "Vypsané termíny na výběr:"
    pohovory_div.appendChild(p)
    for (let p of pohovory) {
        generator(p["iso"], p["pretty"])
    }
}