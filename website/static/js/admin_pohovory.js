import httpGet from "./httpGet.js"
let start_time = document.getElementById("start_time")
let end_time = document.getElementById("end_time")
let pohovory = JSON.parse(httpGet("/send_user/pohovory"))
let content_div = document.getElementById("content")


function seznam_casu() {
    let hodiny = ["7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]
    let minuty = ["00", "20", "40"]
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

function generator(iso, pretty) {
    let row = document.createElement("div")
    row.classList.add("row")
    let col1 = document.createElement("div")
    col1.classList.add("col")
    let col2 = document.createElement("div")
    col2.classList.add("col")
    let smazat_button = document.createElement("button")
    smazat_button.innerHTML = "Smazat"
    smazat_button.classList.add("btn", "btn-danger", "my-1")
    smazat_button.type="submit"
    smazat_button.name = "smazat"
    smazat_button.value = iso

    col1.innerHTML = pretty
    col2.appendChild(smazat_button)
    row.appendChild(col1)
    row.appendChild(col2)
    content_div.appendChild(row)
}

for (let p of pohovory) {
    generator(p["iso"], p["pretty"])
}