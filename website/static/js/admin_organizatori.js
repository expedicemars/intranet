import httpGet from "./httpGet.js"

let organizatori = JSON.parse(httpGet("/admin_api/organizatori"))

function generator_from_db(id, email, jmeno) {
    let row = document.createElement("div")
    row.classList.add("row", "my-2")
    document.getElementById("from_db").appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    row.appendChild(col1)
    col1.innerHTML = id

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    col2.innerHTML = jmeno

    let col3 = document.createElement("div")
    col3.classList.add("col")
    row.appendChild(col3)
    col3.innerHTML = email

    let button = document.createElement("button")
    button.classList.add("btn", "em-button")
    button.type = "button"
    button.innerHTML = "Detail"
    button.name = "result"
    button.value = id
    button.type = "submit"

    let col6 = document.createElement("div")
    col6.classList.add("col-auto")
    row.appendChild(col6)
    col6.appendChild(button)
}

for (let u of organizatori) {
    generator_from_db(u["id"], String(u["email"]), u["jmeno"])
}
