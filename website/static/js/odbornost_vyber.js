import httpGet from "./httpGet.js"
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))

// zadani

for (let odbornost of dostupne_odbornosti) {
    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost.system_name))
    if (zadani.length != 0) {
        for (let filename of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost.system_name + "/" + filename
            a.download = filename
            a.innerHTML = filename
            a.classList.add("link")
            document.getElementById(odbornost.system_name  + "_zadani").appendChild(a)
            document.getElementById(odbornost.system_name  + "_zadani").appendChild(document.createElement("br"))
        }
    } else {
        document.getElementById(odbornost.system_name + "_zadani").innerText = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
    }
}