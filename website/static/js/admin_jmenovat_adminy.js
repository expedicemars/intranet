import httpGet from "./httpGet.js"

let users_from_db = JSON.parse(httpGet("/send_admin/users_from_db"))


function vybrat_usera(id) {
    document.getElementById("result").value = id
    document.getElementById("form").submit()
}

function generator_from_db(target, id, email) {
    let row = document.createElement("div")
    row.classList.add("row", "my-2")
    document.getElementById(target).appendChild(row)

    let col1 = document.createElement("div")
    col1.classList.add("col-auto")
    row.appendChild(col1)
    col1.innerHTML = id

    let col2 = document.createElement("div")
    col2.classList.add("col")
    row.appendChild(col2)
    col2.innerHTML = email

    let button = document.createElement("button")
    button.classList.add("btn", "btn-primary")
    button.type = "button"
    button.innerHTML = "vybrat..."
    button.addEventListener("click", function() {vybrat_usera(id)})

    let col6 = document.createElement("div")
    col6.classList.add("col-auto")
    row.appendChild(col6)
    col6.appendChild(button)
}


// targety: "admins" a "users"
for (let i=0;i<users_from_db.length;i++) {
    let target
    if (users_from_db[i]["role"].includes("admin")) {
        target = "admins"
    } else {
        target = "users"
    }
    generator_from_db(target, users_from_db[i]["id"], String(users_from_db[i]["email"]))
}
