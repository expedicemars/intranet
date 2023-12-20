import httpGet from "./httpGet.js"

let konec_registrace = httpGet("/noauth_api/konec_registrace")
let zacatek_registrace = httpGet("/noauth_api/zacatek_registrace")
let je_zadani_viditelne = httpGet("/admin_api/je_zadani_viditelne")
let je_info_o_konferenci_viditelne = httpGet("/admin_api/je_info_o_konferenci_viditelne")
let koordinator_internetovych_kol = httpGet("/admin_api/koordinator_internetovych_kol")
let aktualni_faze = JSON.parse(httpGet("/noauth_api/aktualni_faze"))
let vsechny_faze = JSON.parse(httpGet("/noauth_api/vsechny_faze"))
let ukoncit_rocnik_button = document.getElementById("ukoncit_rocnik")
let ukoncit_rocnik_input = document.getElementById("ukoncit_rocnik_input")
let toggle_zadani_button = document.getElementById("toggle_zadani")
let stav_zadani = document.getElementById("viditelnost_stav")
let toggle_info_o_konferenci_button = document.getElementById("toggle_info_o_konferenci")
let stav_informace_o_konferenci = document.getElementById("informace_o_konferenci_stav")
let datum_otevreni_input = document.getElementById("datum_otevreni")
let datum_uzavreni_input = document.getElementById("datum_uzavreni")
let exporty = JSON.parse(httpGet("/file_api/exporty_filenames"))
let content_div = document.getElementById("content")
let form = document.getElementById("form")

datum_uzavreni_input.value=konec_registrace
datum_otevreni_input.value=zacatek_registrace
ukoncit_rocnik_button.addEventListener("click", ukoncit)
document.getElementById("koordinator_internetovych_kol").value = koordinator_internetovych_kol



if (je_zadani_viditelne == "True") {
    toggle_zadani_button.innerText = "Skrýt zadání"
    stav_zadani.innerText = "viditelná"
} else {
    toggle_zadani_button.innerText = "Zobrazit zadání"
    stav_zadani.innerText = "skrytá"
}

if (je_info_o_konferenci_viditelne == "True") {
    toggle_info_o_konferenci_button.innerText = "Skrýt stránku"
    stav_informace_o_konferenci.innerText = "viditelná"
} else {
    toggle_info_o_konferenci_button.innerText = "Zobrazit stránku"
    stav_informace_o_konferenci.innerText = "skrytá"
}


for (let faze of vsechny_faze) {
    let opt = document.createElement("option")
    opt.value = faze.system_name
    opt.innerText = faze.display_name
    if (faze.system_name == aktualni_faze.system_name) {
        opt.selected = "selected"
    }
    document.getElementById("faze_select").appendChild(opt)
}


function ukoncit() {
    if (confirm("Chystáš se ukončit ročník, měj zazálohovaný data. Jseš si jistej?")) {
        if (confirm("Vážně? Tohle neni sranda, fakt se to promaže.")) {
            if (confirm("Ještě se prosimtě ujisti, že máš přístup k odevzdanejm projektům a tak.")) {
                if (confirm("Je Michal nejepší?")) {
                    ukoncit_rocnik_input.value = "koncime"
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
    col2.classList.add("col-auto")
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