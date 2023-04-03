import httpGet from "./httpGet.js"
let dostupne_odbornosti = JSON.parse(httpGet("/user_api/dostupne_odbornosti"))
let form = document.getElementById("form")
let odbornost_input = document.getElementById("odbornost")

// vybrani odbornosti
for (let id of dostupne_odbornosti) {
    let node = document.getElementById(id)
    node.addEventListener("click", function() {
        if (confirm("Po vybrání odbornosti už tvoje volba nepůjde změnit. Jasný?")) {
            odbornost_input.value = id
            form.submit()
        }
    })
}

// zadani

for (let odbornost of dostupne_odbornosti) {
    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost))
    if (zadani.length != 0) {
        for (let filename of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost + "/" + filename
            a.download = filename
            a.innerHTML = filename
            document.getElementById(odbornost  + "_zadani").appendChild(a)
            document.getElementById(odbornost  + "_zadani").appendChild(document.createElement("br"))
        }
    } else {
        document.getElementById(odbornost + "_zadani").innerText = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
    }
}