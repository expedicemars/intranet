import httpGet from "../httpGet.js"

let ucastnici = JSON.parse(httpGet("/admin_api/ucastnici"))

function generator_from_db(u) {
    let tr = document.createElement("tr")
    let td1 = document.createElement("td")
    let td2 = document.createElement("td")
    let td3 = document.createElement("td")
    let td4 = document.createElement("td")
    let td5 = document.createElement("td")
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    tr.appendChild(td5)
    document.getElementById("users").appendChild(tr)
    
    td1.innerText = u.jmeno
    td2.innerText = u.email
    td3.innerText = u.datum_registrace
    td4.innerText = u.progress

    let button = document.createElement("button")
    button.classList.add("btn", "em-button")
    button.type = "button"
    button.innerHTML = "Detail"
    button.name = "result"
    button.value = u.id
    button.type = "submit"

    td5.appendChild(button)
}

for (let u of ucastnici) {
    generator_from_db(u)
}
