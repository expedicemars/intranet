import httpGet from "./httpGet.js"
let zacatek_registrace = httpGet("/noauth_api/zacatek_registrace_pretty")
let mit = httpGet("/noauth_api/mit")
let konec_registrace = httpGet("/noauth_api/konec_registrace_pretty")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let odbornosti_div = document.getElementById("odbornosti")

document.getElementById("zacatek_registrace").innerText = zacatek_registrace
document.getElementById("konec_registrace").innerText = konec_registrace
document.getElementById("mit").innerText = mit

// zadani
if (odbornosti_div) {
    for (let odbornost of dostupne_odbornosti) {
        let h3 = document.createElement("h3")
        h3.innerText = odbornost.prvnipmc
        odbornosti_div.appendChild(h3)
        let div = document.createElement("div")
        div.classList.add("border-orange", "rounded-2", "m-2", "p-2", "lighter")
        div.id = odbornost.system_name + "_zadani"
        odbornosti_div.appendChild(div)
    
    }
    
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
}