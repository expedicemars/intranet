import httpGet from "./httpGet.js"
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))

// zadani

for (let odbornost of dostupne_odbornosti) {
    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost))
    if (zadani.length != 0) {
        for (let filename of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost + "/" + filename
            a.download = filename
            a.innerHTML = filename
            a.classList.add("link")
            document.getElementById(odbornost  + "_zadani").appendChild(a)
            document.getElementById(odbornost  + "_zadani").appendChild(document.createElement("br"))
        }
    } else {
        document.getElementById(odbornost + "_zadani").innerText = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
    }
}