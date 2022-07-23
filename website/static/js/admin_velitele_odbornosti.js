import httpGet from "./httpGet.js"
let data = JSON.parse(httpGet("/send_admin/velitel_odbornosti_data"))

// nacteni
let inputs_ids_list = ["biolog", "konstrukter", "fyzik", "inzenyr", "popularizator"]
for (let id of inputs_ids_list) {
    let node = document.getElementById(id)
    if (node) {
        node.value = data[id]
    }
}