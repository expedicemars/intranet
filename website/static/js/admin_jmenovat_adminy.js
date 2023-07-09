import httpGet from "./httpGet.js"

let useri_na_jmenovani_adminu = JSON.parse(httpGet("/admin_api/useri_na_jmenovani_adminu"))


function vybrat_usera(id) {
    document.getElementById("result").value = id
    document.getElementById("form").submit()
}

function generator_from_db(target, id, email, jmeno) {
    let row = document.createElement("div")
    row.classList.add("row", "my-2")
    document.getElementById(target).appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    row.appendChild(col1)
    col1.innerText = id

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    col2.innerText = jmeno

    let col3 = document.createElement("div")
    col3.classList.add("col")
    row.appendChild(col3)
    col3.innerText = email

    let button = document.createElement("button")
    button.classList.add("btn", "em-button")
    button.type = "button"
    button.innerText = "vybrat..."
    button.addEventListener("click", function() {vybrat_usera(id)})

    let col6 = document.createElement("div")
    col6.classList.add("col-auto")
    row.appendChild(col6)
    col6.appendChild(button)
}


for (let u of useri_na_jmenovani_adminu["admins"]) {
    generator_from_db("admins", u["id"], String(u["email"]), u["jmeno"])
}
for (let u of useri_na_jmenovani_adminu["users"]) {
    generator_from_db("users", u["id"], String(u["email"]), u["jmeno"])
}