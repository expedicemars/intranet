import httpGet from "./httpGet.js"

let button_ids = ["biolog", "fyzik", "konstrukter", "inzenyr", "popularizator"]
let form = document.getElementById("form")
let result = document.getElementById("result")
let kontakt = httpGet("/send_user/kontakt_na_meho_velitele_odbornosti")

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

let kontakt_span = document.getElementById("kontakt")
if (kontakt_span) {
    console.log(kontakt)
    kontakt_span.innerHTML = kontakt
}

