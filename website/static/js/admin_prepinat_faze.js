import httpGet from "./httpGet.js"

let faze = JSON.parse(httpGet("/send_admin/faze"))
let mailing_list_div = document.getElementById("mailing_list")
let upozornit_na_zadani_div = document.getElementById("upozornit_na_zadani")
let prehled_div = document.getElementById("prehled")
let aktualni_nadpis = document.getElementById("aktualni_nadpis")
let predchozi_faze_btn = document.getElementById("predchozi_faze_btn")
let dalsi_faze_btn = document.getElementById("dalsi_faze_btn")
let result_input = document.getElementById("result")
let form = document.getElementById("form")

predchozi_faze_btn.addEventListener("click", function() {odeslat("predchozi")})
dalsi_faze_btn.addEventListener("click", function() {odeslat("dalsi")})

// přehled fází
for (let fa of faze) {
    let div = document.createElement("div")
    div.classList.add("border", "rounded-2", "border-secondary", "m-2", "p-2")
    if (fa["active"]) {
        div.classList.add("aktivni-faze")
    }
    prehled_div.appendChild(div)

    let code = document.createElement("code")
    code.innerHTML = fa["nazev"]
    div.appendChild(code)
    
    let popis = document.createElement("p")
    popis.innerHTML = fa["popis"]
    div.appendChild(popis)
}

// prepinac
let aktualni_faze
for (let fa of faze) {
    if (fa["active"] == true) {
        aktualni_faze = fa
        break
    }
}

let nadpis = "Aktuální fáze: " + aktualni_faze["nazev"]
aktualni_nadpis.innerHTML = nadpis

if (aktualni_faze["nazev"] == "otevrene_registrace") {
    let emails = httpGet("/send_admin/mailing_list")
    document.getElementById("mailing_list_content").innerHTML = JSON.parse(emails)
    mailing_list_div.hidden = false
    upozornit_na_zadani_div.hidden = true
    predchozi_faze_btn.hidden =  true
    dalsi_faze_btn.innerHTML = "Zpřístupnit zadání"
} else if (aktualni_faze["nazev"] == "zpristupnena_zadani") {
    let emails = httpGet("/send_admin/upozornit_na_zadani")
    document.getElementById("upozornit_na_zadani_content").innerHTML = JSON.parse(emails)
    upozornit_na_zadani_div.hidden = false
    predchozi_faze_btn.hidden =  false
    mailing_list_div.hidden = true
    dalsi_faze_btn.innerHTML = "Uzavřít registrace"
} else if (aktualni_faze["nazev"] == "uzavrene_registrace") {
    predchozi_faze_btn.hidden =  false
    upozornit_na_zadani_div.hidden = true
    mailing_list_div.hidden = true
    dalsi_faze_btn.innerHTML = "Ukončit ročník"
} else if (aktualni_faze["nazev"] == "ukonceny_rocnik") {
    predchozi_faze_btn.hidden =  true
    upozornit_na_zadani_div.hidden = true
    mailing_list_div.hidden = true
    dalsi_faze_btn.innerHTML = "Otevřít registrace a začít nový ročník"
}



// odeslani pozadavku na server o prepnuti faze
function odeslat(jak) {
    if (aktualni_faze["nazev"] == "uzavrene_registrace" && jak == "dalsi") {
        if (confirm("Chystáš se ukončit ročník, zazálohovat a smazat data. Jseš si jistej?")) {
            if (confirm("Vážně? Tohle neni sranda, fakt se to promaže. I deadliny budou pryč.")) {
                if (confirm("Ještě se prosimtě ujisti, že máš přístup k odevzdanejm projektům a motivákům a tak.")) {
                    if (confirm("Je Michal nejepší?")) {
                        result_input.value = jak
                        form.submit()
                    }
                }
            }
        }
    } else {
        result_input.value = jak
        form.submit()
    }
}

