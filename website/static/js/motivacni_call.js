import httpGet from "./httpGet.js"
let pohovory = JSON.parse(httpGet("/user_api/volne_pohovory"))
let aktualne = JSON.parse(httpGet("/user_api/datum_motivacniho_callu"))
let hodiny = JSON.parse(httpGet("/user_api/limit_hodin"))["limit"]
let link_p = document.getElementById("link")
let jsou_pohovory_div = document.getElementById("jsou_pohovory")
let nejsou_pohovory_div = document.getElementById("nejsou_pohovory")
let datum_je = document.getElementById("datum_je")
let datum_neni = document.getElementById("datum_neni")
let datum_span = document.getElementById("datum_span")
let pohovory_table = document.getElementById("pohovory")
let terminy_div = document.getElementById("terminy")

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

if (aktualne["datum"]) {
    datum_je.hidden = false
    datum_span.innerText = aktualne["datum"]
} else {
    datum_neni.hidden = false
    if (terminy_div) {
        terminy_div.hidden = false
    }
}

function generator(id, pretty) {
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
    zapsat_button.value = id
    td.appendChild(zapsat_button)
}

if (pohovory.length == 0 || aktualne["datum"]) {
    if (nejsou_pohovory_div) {
        nejsou_pohovory_div.hidden = false
    }
} else {
    if (jsou_pohovory_div) {
        jsou_pohovory_div.hidden = false
        for (let p of pohovory) {
            generator(p["id"], p["pretty"])
        }
    }
}

document.getElementById("hodiny_1").innerText = hodiny
document.getElementById("hodiny_2").innerText = hodiny