import httpGet from "./httpGet.js"

let button_ids = ["biolog", "fyzik", "konstrukter", "inzenyr", "popularizator"]
let form = document.getElementById("form")
let result = document.getElementById("result")
let kontakt = httpGet("/user_api/kontakt_na_meho_velitele_odbornosti")


// vybrani odbornosti
for (let id of button_ids) {
    let node = document.getElementById(id)
    if (node){
        node.addEventListener("click", function() {
            if (confirm("Po vybrání odbornosti už tvoje volba nepůjde změnit. Jasný?")) {
                result.value = id
                form.submit()
            }
        })
    }
}

// kontaktní
let kontakt_span = document.getElementById("kontakt")
if (kontakt_span) {
    kontakt_span.innerHTML = kontakt
}

// zadani
let odbornost_current_usera = document.getElementById("odbornost").value // MUZE Obsahovat pythoni False
if (odbornost_current_usera == "False") {
    odbornost_current_usera = false
}

if (odbornost_current_usera) {
    let zadani = JSON.parse(httpGet("/send_zadani/" + odbornost_current_usera + "/__jmena"))
        if (zadani) {
            for (let zadani_file of zadani) {
                let a = document.createElement("a")
                a.href = "/send_zadani/"+ odbornost_current_usera + "/" + zadani_file
                a.download = zadani_file
                a.innerHTML = zadani_file
                document.getElementById("zadani_single").appendChild(a)
                document.getElementById("zadani_single").appendChild(document.createElement("br"))
            }
        } else {
            document.getElementById("zadani_single").innerHTML = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
        }
} else {
    for (let odbornost of button_ids) {
        let zadani = JSON.parse(httpGet("/send_zadani/" + odbornost + "/__jmena"))
        if (zadani) {
            for (let zadani_file of zadani) {
                let a = document.createElement("a")
                a.href = "/send_zadani/"+ odbornost + "/" + zadani_file
                a.download = zadani_file
                a.innerHTML = zadani_file
                document.getElementById(odbornost  + "_zadani").appendChild(a)
                document.getElementById(odbornost  + "_zadani").appendChild(document.createElement("br"))
            }
        } else {
            document.getElementById(odbornost + "_zadani").innerHTML = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
        }
    }
} 

// prace

let prace = JSON.parse(httpGet("/send_prace_filenames"))
let nahrat_praci_div = document.getElementById("nahrat_praci")
let ukazat_praci_div = document.getElementById("ukazat_praci")
let ukazat_praci_content_div = document.getElementById("ukazat_praci_content")
if (prace) {
    nahrat_praci_div.hidden = true
    ukazat_praci_div.hidden = false
    for (let prace_file of prace) {
        let a = document.createElement("a")
        a.href = "/send_prace_file/" + prace_file
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