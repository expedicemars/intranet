import httpGet from "./httpGet.js"

let users_from_db = JSON.parse(httpGet("/send_admin/users_from_db"))


function smazat_usera(id) {
    document.getElementById("result").value = id
    document.getElementById("form").submit()
}

function generator_from_db(id, email, last_login, confirmed, role) {
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
    col2.innerHTML = email

    let col3 = document.createElement("div")
    col3.classList.add("col")
    row.appendChild(col3)
    col3.innerHTML = last_login

    let col4 = document.createElement("div")
    col4.classList.add("col")
    row.appendChild(col4)
    col4.innerHTML = confirmed

    let col5 = document.createElement("div")
    col5.classList.add("col")
    row.appendChild(col5)
    col5.innerHTML = role

    let button = document.createElement("button")
    button.classList.add("btn", "btn-danger")
    button.type = "button"
    button.innerHTML = "smazat usera"
    button.addEventListener("click", function() {smazat_usera(id)})

    let col6 = document.createElement("div")
    col6.classList.add("col-auto")
    row.appendChild(col6)
    col6.appendChild(button)
}

for (let i=0;i<users_from_db.length;i++) {
    generator_from_db(users_from_db[i]["id"], String(users_from_db[i]["email"]), users_from_db[i]["last_login"], users_from_db[i]["confirmed"], users_from_db[i]["role"])
}
