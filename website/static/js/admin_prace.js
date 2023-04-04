import httpGet from "./httpGet.js"

let data = JSON.parse(httpGet("/admin_api/data_pro_prace"))
let content_div = document.getElementById("content")


function generator(zaznam_o_jednom) {
    content_div.appendChild(document.createElement("hr"))
    let row = document.createElement("div")
    content_div.appendChild(row)
    row.classList.add("row")

    let jmeno_col = document.createElement("div")
    row.appendChild(jmeno_col)
    jmeno_col.classList.add("col-sm")
    if (zaznam_o_jednom["jmeno"]) {
        let a = document.createElement("a")
        a.href = "/admin/detail_usera/" + String(zaznam_o_jednom["id"])
        jmeno_col.appendChild(a)
        let jmeno = document.createElement("h3")
        jmeno.innerHTML = zaznam_o_jednom["jmeno"]
        a.appendChild(jmeno)
    } else {
        jmeno_col.innerHTML = "Ještě nezadal jméno"
    }

    let prace_col = document.createElement("div")
    row.appendChild(prace_col)
    prace_col.classList.add("col-sm")
    if (zaznam_o_jednom["prace"].length == 0) {
        prace_col.innerHTML = "Ještě nenahrál práci"
    } else {
        for (let filename of zaznam_o_jednom["prace"]) {
            let a = document.createElement("a")
            a.innerHTML = filename
            a.download = filename
            a.href = "/file_api/cizi_prace/" + String(zaznam_o_jednom["id"]) + "/" + filename
            prace_col.appendChild(a)
            prace_col.appendChild(document.createElement("br"))
        }
    }
}

for (let zaznam of data) {
    generator(zaznam)
}