import httpGet from "./httpGet.js"
let odbornosti_kterym_velim = JSON.parse(httpGet("/admin_api/odbornosti_kterym_velim"))
let data = JSON.parse(httpGet("/admin_api/velitel_odbornosti_data"))

// za kazdou odbornost, ktery velim, getnu jeji data o zadani n stuff, skryju divy nebo vygeneruju a href linky
for (let odbornost of odbornosti_kterym_velim) {
    let nahrat_zadani_div = document.getElementById(odbornost + "_nahrat_zadani")
    let ukazat_zadani_div = document.getElementById(odbornost + "_ukazat_zadani")
    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost))
    if (zadani.length != 0) {
        nahrat_zadani_div.hidden = true
        ukazat_zadani_div.hidden = false
        for (let zadani_file of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost + "/" + zadani_file
            a.download = zadani_file
            a.innerHTML = zadani_file
            ukazat_zadani_div.appendChild(a)
            ukazat_zadani_div.appendChild(document.createElement("br"))
        }
    } else {
        nahrat_zadani_div.hidden = false
        ukazat_zadani_div.hidden = true
    }

}

// nacteni
for (let odbornost of odbornosti_kterym_velim) {
    document.getElementById(odbornost).value = data[odbornost]
}

