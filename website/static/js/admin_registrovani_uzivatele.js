import httpGet from "./httpGet.js"

let ucastnici = JSON.parse(httpGet("/admin_api/ucastnici"))

function generator_from_db(id, email, jmeno) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    let td4 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    document.getElementById("users").appendChild(tr)
    
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

for (let u of ucastnici) {
    generator_from_db(u["id"], String(u["email"]), u["jmeno"])
}
