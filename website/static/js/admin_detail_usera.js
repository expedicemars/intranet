import httpGet from "./httpGet.js"
let id_usera = document.getElementById("id").value
let detail_usera = JSON.parse(httpGet("/send_admin/detail_usera_" + String(id_usera)))
let motivak_bool = httpGet("/send_motivak/" + String(id_usera) + "/name")
let prace_filenames = JSON.parse(httpGet("/send_prace_filenames/" + String(id_usera)))



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

if (motivak_bool) {
    document.getElementById("motivak_download").hidden = false
    document.getElementById("motivak_disclaimer").hidden = true
} else {
    document.getElementById("motivak_download").hidden = true
    document.getElementById("motivak_disclaimer").hidden = false
}


if (prace_filenames) {
    document.getElementById("prace_disclaimer").hidden = true
    let prace_div = document.getElementById("prace_div")
    for (let filename of prace_filenames) {
        let a = document.createElement("a")
        a.innerHTML = filename
        a.download = filename
        a.href = "/send_prace_file/" + String(id_usera) + "/" + filename
        prace_div.appendChild(a)
        prace_div.appendChild(document.createElement("br"))
    }
} else {
    document.getElementById("prace_disclaimer").hidden = false
}
