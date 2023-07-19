import httpGet from "./httpGet.js"
let pohovory = JSON.parse(httpGet("/user_api/volne_pohovory"))
let aktualne = JSON.parse(httpGet("/user_api/datum_pohovoru"))
let datum_p = document.getElementById("datum")
let link_p = document.getElementById("link")
let jsou_pohovory_div = document.getElementById("jsou_pohovory")
let nejsou_pohovory_div = document.getElementById("nejsou_pohovory")
let pohovory_table = document.getElementById("pohovory")

if (aktualne["datum"]) {
    datum_p.innerHTML = "Momentálně máš vybrané tohle datum: " + aktualne["datum"]
} else {
    datum_p.innerHTML = "Momentálně nemáš vybrané žádné datum pohovoru."
}

if (aktualne["link"]) {
    let a = document.createElement("a")
    a.classList.add("link")
    a.innerHTML = "Odkaz na meeting"
    a.href = aktualne["link"]
    a.target = "blank"
    link_p.appendChild(a)
} else {
    link_p.innerHTML = "Zatím tu nemáš odkaz na pohovor. Až ho organizátoři vytvoří, čekej ho buď tady, nebo na e-mailu."
}


function generator(iso, pretty) {
    let tr = document.createElement("tr")
    let th = document.createElement("th")
    let td = document.createElement("td")
    pohovory_table.appendChild(tr)
    tr.appendChild(th)
    tr.appendChild(td)
    th.innerText = pretty
    
    let zapsat_button = document.createElement("button")
    zapsat_button.innerHTML = "Zapsat tento termín"
    zapsat_button.classList.add("btn", "em-button")
    zapsat_button.type="submit"
    zapsat_button.name = "vybrat"
    zapsat_button.value = iso
    td.appendChild(zapsat_button)
}

if (pohovory.length == 0) {
    nejsou_pohovory_div.hidden = false
} else {
    jsou_pohovory_div.hidden = false
    for (let p of pohovory) {
        generator(p["iso"], p["pretty"])
    }
}