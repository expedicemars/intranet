import httpGet from "./httpGet.js"
let start_time = document.getElementById("start_time")
let end_time = document.getElementById("end_time")
let pohovory = JSON.parse(httpGet("/admin_api/pohovory"))
let content_table = document.getElementById("content")
let prihlaseni_table = document.getElementById("prihlaseni")

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
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    content_table.appendChild(tr)

    td1.innerText = pretty
    td2.innerText = admin

    if (user) {
        td3.innerText = "Obsazeno"
    } else {
        let smazat_button = document.createElement("button")
        smazat_button.innerHTML = "Smazat"
        smazat_button.classList.add("btn", "btn-danger")
        smazat_button.type="submit"
        smazat_button.name = "smazat"
        smazat_button.value = iso
        td3.appendChild(smazat_button)
    }
}

function generator_prihlasenych(jmeno, pretty, id, link, admin) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    let td4 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    content_table.appendChild(tr)
    
    td1.innerText = pretty

    let a = document.createElement("a")
    a.href = "/admin/detail_usera/" + String(id)
    a.innerHTML = jmeno
    a.classList.add("link")
    td2.appendChild(a)
    
    td3.innerText = admin
    
    if (link) {
        let a2 = document.createElement("a")
        td4.appendChild(a2)
        a2.innerHTML = "Odkaz na meeting"
        a2.href = link
        a2.target = "blank"
        a2.classList.add("link")
    } else {
        td4.innerHTML = "Tady link ještě není"
    }
    

    prihlaseni_table.append(tr)
}

for (let p of pohovory) {
    generator_vypsanych(p["iso"], p["pretty"], p["user"], p["admin"])
    if (p["user"]) {
        generator_prihlasenych(p["jmeno"], p["pretty"], p["user"], p["link"], p["admin"])
    }
}

