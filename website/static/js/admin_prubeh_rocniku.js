import httpGet from "./httpGet.js"

let registrace = httpGet("/noauth_api/registrace")
let je_registrace_otevrena = httpGet("/admin_api/je_registrace_otevrena")
let mailing_list = httpGet("/admin_api/mailing_list")
let ukoncit_rocnik_button = document.getElementById("ukoncit_rocnik")
let ukoncit_rocnik_input = document.getElementById("ukoncit_rocnik_input")
let toggle_registraci_button = document.getElementById("toggle_registraci")
let registrace_date_input = document.getElementById("registrace_date")
let exporty = JSON.parse(httpGet("/file_api/exporty_filenames"))
let content_div = document.getElementById("content")
let form = document.getElementById("form")
registrace_date_input.value=registrace
ukoncit_rocnik_button.addEventListener("click", ukoncit)
document.getElementById("mailing_list").innerHTML = JSON.parse(mailing_list)

if (je_registrace_otevrena == "True") {
    toggle_registraci_button.innerHTML = "Uzavřít registraci"
} else {
    toggle_registraci_button.innerHTML = "Otevřít registraci"
}




function ukoncit() {
    if (confirm("Chystáš se ukončit ročník, měj zazálohovaný data. Jseš si jistej?")) {
        if (confirm("Vážně? Tohle neni sranda, fakt se to promaže.")) {
            if (confirm("Ještě se prosimtě ujisti, že máš přístup k odevzdanejm projektům a tak.")) {
                if (confirm("Je Michal nejepší?")) {
                    ukoncit_rocnik_input.value = "koncime"
                    console.log(ukoncit_rocnik_input.value)
                    console.log(ukoncit_rocnik_input)
                    form.submit()
                }
            }
        }
    }
}

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
    a.href = "/file_api/export/" + filename
    a.classList.add("link")
    col1.appendChild(a)

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)

    let btn = document.createElement("button")
    btn.classList.add("btn", "btn-danger")
    btn.innerHTML = "Smazat export"
    btn.type = "submit"
    btn.name = "smazat_export"
    btn.value = isoformat
    col2.appendChild(btn)
}

for (let zaznam of exporty) {
    generator(zaznam["iso"], zaznam["datum"], zaznam["filename"])
}