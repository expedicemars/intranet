import httpGet from "./httpGet.js"
let id_usera = document.getElementById("id").value
let detail_usera = JSON.parse(httpGet("/send_admin/detail_usera_" + String(id_usera)))
let motivak_bool = httpGet("/send_motivak/" + String(id_usera) + "/name")
//todo prace_bool a prace_names a zmenit vsechno aby pouzivalo /send_motivak

for (let key in detail_usera) {
    let node = document.getElementById(key)
    if (node) {
        if (key == "id") {
            document.getElementById("id_display").innerHTML = detail_usera[key]
        } else {
            node.innerHTML = detail_usera[key]
        }
    }
}

if (motivak_bool != "missing") {
    document.getElementById("motivak_download").hidden = false
    document.getElementById("motivak_disclaimer").hidden = true
} else {
    document.getElementById("motivak_download").hidden = true
    document.getElementById("motivak_disclaimer").hidden = false
}