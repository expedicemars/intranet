import httpGet from "./httpGet.js"
let start_time = document.getElementById("start_time")
let end_time = document.getElementById("end_time")
let pohovory = JSON.parse(httpGet("/admin_api/motivacni_cally"))
let content_table = document.getElementById("content")
let prihlaseni_table = document.getElementById("prihlaseni")
let probehly_table = document.getElementById("probehly")
let form = document.getElementById("form")
let smazat_button = document.getElementById("smazat_vybrane")
let result_input = document.getElementById("result")

smazat_button.addEventListener("click", vyhodnotit)

let hodiny = ["7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]
let minuty = ["00","15","30","45"]
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

function vyhodnotit() {
    result = []
    let checkboxes = document.getElementsByName("smazat")
    for (let ch of checkboxes) {
        if (ch.checked) {
            result.push(ch.value)
        }
    }
    if (result.length == 0) {
        alert("Nebyly zvoleny žádné cally.")
    } else {
        result_input.value = JSON.stringify(result)
        form.submit()
    }
}

function generator_vypsanych(id, pretty, user_id, admin_email) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    content_table.appendChild(tr)

    td1.innerText = pretty
    td2.innerText = admin_email
    td3.classList.add("text-center")

    if (user_id) {
        td3.innerText = "Obsazeno"
    } else {
        let checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.name = "smazat"
        checkbox.value = id
        checkbox.classList.add("form-check-input")
        td3.appendChild(checkbox)
    }
}

function generator_prihlasenych(jmeno, pretty, user_id, link, admin_email) {
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
    a.href = "/admin/detail_usera/" + String(user_id)
    a.innerHTML = jmeno
    a.classList.add("link")
    td2.appendChild(a)
    
    td3.innerText = admin_email
    
    if (link) {
        let a2 = document.createElement("a")
        td4.appendChild(a2)
        a2.innerHTML = "Odkaz na meeting"
        a2.href = link
        a2.target = "blank"
        a2.classList.add("link")
    } else {
        td4.innerHTML = "Tady link ještě není. "
        let a3 = document.createElement("a")
        a3.href = "/admin/detail_usera/" + String(user_id) + "#link"
        a3.innerHTML = "Přidat link"
        a3.classList.add("link")
        td4.appendChild(a3)
    }
    

    prihlaseni_table.append(tr)
}

function generator_probehlych(jmeno, pretty, user_id) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    content_table.appendChild(tr)
    
    td1.innerText = pretty

    let a = document.createElement("a")
    a.href = "/admin/detail_usera/" + String(user_id)
    a.innerHTML = jmeno
    a.classList.add("link")
    td2.appendChild(a)

    probehly_table.append(tr)
}

for (let p of pohovory) {
    if (p["probehl"]) {
        generator_probehlych(p["jmeno"], p["pretty"], p["user_id"])
    } else {
        generator_vypsanych(p["id"], p["pretty"], p["user_id"], p["admin_email"])
        if (p["user_id"]) {
            generator_prihlasenych(p["jmeno"], p["pretty"], p["user_id"], p["link"], p["admin_email"])
        }
    }
}

