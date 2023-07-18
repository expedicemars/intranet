import httpGet from "./httpGet.js"
let start_time = document.getElementById("start_time")
let end_time = document.getElementById("end_time")
let pohovory = JSON.parse(httpGet("/admin_api/pohovory"))
let content_div = document.getElementById("content")
let prihlaseni_div = document.getElementById("prihlaseni")

function seznam_casu() {
    let hodiny = ["7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]
    let minuty = ["00","10","20","30","40","50"]
    for (let h of hodiny) {
        for (let m of minuty) {
            let opt = document.createElement("option")
            let value = h + ":" + m
            opt.value = value
            opt.innerHTML = value
            start_time.appendChild(opt.cloneNode(true))
            end_time.appendChild(opt.cloneNode(true))
        }
    }
}

seznam_casu()

function generator_vypsanych(iso, pretty, user, admin) {
    let row = document.createElement("div")
    row.classList.add("row")
    let col1 = document.createElement("div")
    col1.classList.add("col")
    let col2 = document.createElement("div")
    col2.classList.add("col")
    let col3 = document.createElement("div")
    col3.classList.add("col")
    if (user) {
        col3.innerHTML = "Obsazeno"
    } else {
        let smazat_button = document.createElement("button")
        smazat_button.innerHTML = "Smazat"
        smazat_button.classList.add("btn", "btn-danger", "my-1")
        smazat_button.type="submit"
        smazat_button.name = "smazat"
        smazat_button.value = iso
        col3.appendChild(smazat_button)
    }

    col1.innerHTML = pretty
    col2.innerHTML = admin
    row.appendChild(col1)
    row.appendChild(col2)
    row.appendChild(col3)
    content_div.appendChild(row)
}

function generator_prihlasenych(jmeno, pretty, id, link, admin) {
    let row = document.createElement("div")
    row.classList.add("row")
    
    let col1 = document.createElement("div")
    row.appendChild(col1)
    col1.classList.add("col")
    col1.innerHTML = pretty

    let col2 = document.createElement("div")
    row.appendChild(col2)
    col2.classList.add("col")
    let a = document.createElement("a")
    col2.appendChild(a)
    a.href = "/admin/detail_usera/" + String(id)
    a.innerHTML = jmeno
    a.classList.add("link")

    let col25 = document.createElement("div")
    row.appendChild(col25)
    col25.classList.add("col")
    col25.innerText = admin
    
    let col3 = document.createElement("div")
    row.appendChild(col3)
    col3.classList.add("col")
    if (link) {
        let a2 = document.createElement("a")
        col3.appendChild(a2)
        a2.innerHTML = "Odkaz na meeting"
        a2.href = link
        a2.target = "blank"
        a2.classList.add("link")
    } else {
        col3.innerHTML = "Tady link ještě není"
    }
    

    prihlaseni_div.append(row)
}

for (let p of pohovory) {
    generator_vypsanych(p["iso"], p["pretty"], p["user"], p["admin"])
    if (p["user"]) {
        generator_prihlasenych(p["jmeno"], p["pretty"], p["user"], p["link"], p["admin"])
    }
}

