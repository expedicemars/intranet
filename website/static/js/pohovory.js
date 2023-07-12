import httpGet from "./httpGet.js"
let pohovory = JSON.parse(httpGet("/user_api/volne_pohovory"))
let aktualne = JSON.parse(httpGet("/user_api/datum_pohovoru"))
let datum_p = document.getElementById("datum")
let link_p = document.getElementById("link")
let pohovory_div = document.getElementById("pohovory")

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
    let row = document.createElement("div")
    row.classList.add("row")
    let col1 = document.createElement("div")
    col1.classList.add("col")
    let col2 = document.createElement("div")
    col2.classList.add("col")
    let zapsat_button = document.createElement("button")
    zapsat_button.innerHTML = "Zapsat tento termín"
    zapsat_button.classList.add("btn", "em-button", "my-1")
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
    pohovory_div.innerHTML = "Nejsou vypsané žádné termíny online setkání."
} else {
    let p = document.createElement("p")
    p.innerHTML = "Tady si můžeš vybrat termín online setkání. Po výběu je možné svojí volbu změnit:"
    pohovory_div.appendChild(p)
    for (let p of pohovory) {
        generator(p["iso"], p["pretty"])
    }
}