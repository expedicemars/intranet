import httpGet from "./httpGet.js"

let button_ids = ["biolog", "fyzik", "konstrukter", "inzenyr", "popularizator"]
let form = document.getElementById("form")
let result = document.getElementById("result")
let kontakt = httpGet("/send_user/kontakt_na_meho_velitele_odbornosti")


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
                a.href = "/send_zadani/"+ odbornost + "/" + zadani_file
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
