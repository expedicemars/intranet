import httpGet from "./httpGet.js"

let detail_usera = JSON.parse(httpGet("/send_admin/detail_usera_"+document.getElementById("id").value))

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