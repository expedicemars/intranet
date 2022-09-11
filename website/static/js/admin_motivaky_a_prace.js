import httpGet from "./httpGet.js"

let data = JSON.parse(httpGet("/send_admin/data_pro_motivaky_a_prace"))
let content_div = document.getElementById("content")
let b1 = document.getElementById("b1")
let b2 = document.getElementById("b2")
b1.addEventListener("click", vyhodnotit)
b2.addEventListener("click", vyhodnotit)



function generator(zaznam_o_jednom) {
    content_div.appendChild(document.createElement("hr"))
    let row = document.createElement("div")
    content_div.appendChild(row)
    row.classList.add("row")

    let jmeno_col = document.createElement("div")
    row.appendChild(jmeno_col)
    jmeno_col.classList.add("col-sm")
    if (zaznam_o_jednom["jmeno"]) {
        let jmeno = document.createElement("h3")
        jmeno.innerHTML = zaznam_o_jednom["jmeno"]
        jmeno_col.appendChild(jmeno)
    } else {
        jmeno_col.innerHTML = "Ještě nezadal jméno"
    }

    let motivak_col = document.createElement("div")
    row.appendChild(motivak_col)
    motivak_col.classList.add("col-sm")
    if (zaznam_o_jednom["motivak"]) {
        let a = document.createElement("a")
        motivak_col.appendChild(a)
        a.innerHTML = "Stáhnout motivák"
        a.href = "/send_motivak/" + String(zaznam_o_jednom["id"]) + "/file"
        a.download = "motivak"
    } else {
        motivak_col.innerHTML = "Ještě nenahrál motivák"
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
            a.href = "/send_prace_file/" + String(zaznam_o_jednom["id"]) + "/" + filename
            prace_col.appendChild(a)
            prace_col.appendChild(document.createElement("br"))
        }
    }

    let label = document.createElement("label")
    content_div.appendChild(label)
    label.for = String(zaznam_o_jednom["id"])
    label.innerHTML = "Hodnocení motiváku. Můžeš sem psát poznámky, postřehy, otázky k pohovoru:"

    let textarea = document.createElement("textarea")
    textarea.id = zaznam_o_jednom["id"]
    textarea.classList.add("form-control")
    textarea.rows = 5
    content_div.appendChild(textarea)
    textarea.value = zaznam_o_jednom["hodnoceni"]


    let s = document.createElement("span")
    content_div.appendChild(s)
    s.innerHTML = String(textarea.value.length) + "/5000"
    textarea.addEventListener("input", function() {
        s.innerHTML = String(this.value.length) + "/5000"
    })
}

for (let zaznam of data) {
    generator(zaznam)
}

function vyhodnotit() {
    let result = []
    for (let zaznam of data) {
        let z = {}
        z["id"] = zaznam["id"]
        z["hodnoceni"] = document.getElementById(zaznam["id"]).value
        result.push(z)
    }
    document.getElementById("result").value = JSON.stringify(result)
    document.getElementById("form").submit()
} 