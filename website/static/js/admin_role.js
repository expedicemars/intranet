import httpGet from "./httpGet.js"
import TableCreator from "./table_creator.js";

let useri_na_jmenovani_adminu = JSON.parse(httpGet("/admin_api/useri_na_jmenovani_adminu"))
let prehled_roli = JSON.parse(httpGet("/admin_api/prehled_roli"))

function generator_from_db(target, id, email, jmeno) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    let td4 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    document.getElementById(target).appendChild(tr)
    
    td1.innerText = id
    td2.innerText = jmeno
    td3.innerText = email

    let button = document.createElement("button")
    button.classList.add("btn", "em-button")
    button.type = "button"
    button.innerHTML = "Detail"
    button.name = "result"
    button.value = id
    button.type = "submit"

    td4.appendChild(button)
}


for (let u of useri_na_jmenovani_adminu["admins"]) {
    generator_from_db("admins", u["id"], String(u["email"]), u["jmeno"])
}
for (let u of useri_na_jmenovani_adminu["users"]) {
    generator_from_db("users", u["id"], String(u["email"]), u["jmeno"])
}

let tc = new TableCreator(document.getElementById("role_table"))
tc.make_header(["role", "počet adminů", "admini"])
tc.make_tbody()
for (let r of prehled_roli) {
    tc.make_row([r.role, r.emails.length, r.emails.join(", ")])
}