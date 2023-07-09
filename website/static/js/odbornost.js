import httpGet from "./httpGet.js"

let kontakt = httpGet("/user_api/kontakt_na_meho_velitele_odbornosti")
document.getElementById("kontakt").innerText = kontakt

let zadani = JSON.parse(httpGet("/file_api/zadani_filenames_me_odbornosti"))
if (zadani.length != 0) {
    for (let zadani_file of zadani) {
        let a = document.createElement("a")
        a.classList.add("link")
        a.href = "/file_api/zadani_file_me_odbornosti/" + zadani_file
        a.download = zadani_file
        a.innerHTML = zadani_file
        document.getElementById("zadani_single").appendChild(a)
        document.getElementById("zadani_single").appendChild(document.createElement("br"))
    }
} else {
    document.getElementById("zadani_single").innerHTML = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
}

// prace
let prace = JSON.parse(httpGet("/file_api/send_filenames_vlastni_prace"))
let nahrat_praci_div = document.getElementById("nahrat_praci")
let ukazat_praci_div = document.getElementById("ukazat_praci")
let ukazat_praci_content_div = document.getElementById("ukazat_praci_content")
if (prace) {
    nahrat_praci_div.hidden = true
    ukazat_praci_div.hidden = false
    for (let prace_file of prace) {
        let a = document.createElement("a")
        a.classList.add("link")
        a.href = "/file_api/vlastni_prace/" + prace_file
        a.download = prace_file
        a.innerHTML = prace_file
        ukazat_praci_content_div.appendChild(a)
        ukazat_praci_content_div.appendChild(document.createElement("br"))
    }
} else {
    nahrat_praci_div.hidden = false
    ukazat_praci_div.hidden = true
}

document.getElementById("nahrana_prace").addEventListener("change", function() {
    let spolecna_velikost = 0
    for (let file of this.files) {
        spolecna_velikost += file.size
    }
    if (spolecna_velikost > 20000000) {
        alert("Zajisti prosím, aby celková velikost tvývh souborů nebyla přes 20 MB. Pokud potřebuješ více místa, použij prosím jakékoli cloudové úložiště a sem nám pošli textový dokument, ve kterém bude sdílecí link.")
        this.value = "";
    }

})