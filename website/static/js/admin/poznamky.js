import httpGet from "../httpGet.js"
let textarea = document.getElementById("nova_poznamka")
let zapsat_poznamku = document.getElementById("zapsat")
let ulozit_button = document.getElementById("ulozit")
let form = document.getElementById("form")
let result_input = document.getElementById("result")
let content_div = document.getElementById("poznamky")
let poznamky = JSON.parse(httpGet("/admin_api/poznamky"))
let username = document.getElementById("username").value
let date = document.getElementById("date").value


ulozit_button.addEventListener("click", vyhodnotit)
zapsat_poznamku.addEventListener("click", function() {
    generator(username, date, textarea.value)
})


function vyhodnotit() {
    let result = []
    for (let pdiv of content_div.childNodes) {
        let zaznam = {}
        zaznam["autor"] = pdiv.childNodes[0].childNodes[0].innerHTML.replace("Autor: ", "")
        zaznam["datum"] = pdiv.childNodes[0].childNodes[1].innerHTML.replace("Datum: ", "")
        zaznam["msg"] = pdiv.childNodes[1].innerHTML
        result.push(zaznam)
    }
    result_input.value = JSON.stringify(result)
    form.submit()
}

function generator(autor, datum, msg) {
    let div = document.createElement("div")
    div.classList.add("border-orange", "rounded-2", "m-2", "p-2", "lighter")
    let row = document.createElement("div")
    row.classList.add("row")
    let col1 = document.createElement("div")
    col1.classList.add("col")
    col1.innerHTML = "Autor: " + autor
    let col2 = document.createElement("div")
    col2.classList.add("col")
    col2.innerHTML = "Datum: " + datum
    let col3 = document.createElement("div")
    col3.classList.add("col")
    let smazat_button = document.createElement("button")
    smazat_button.type = "button"
    smazat_button.classList.add("btn", "btn-outline-danger", "float-end")
    smazat_button.innerHTML = "Smazat poznámku"
    smazat_button.addEventListener("click", function() {
        this.parentElement.parentElement.parentElement.remove()
    })
    let p = document.createElement("p")
    p.innerText = msg

    content_div.appendChild(div)
    div.appendChild(row)
    div.appendChild(p)
    row.appendChild(col1)
    row.appendChild(col2)
    row.appendChild(col3)
    col3.appendChild(smazat_button)
}

for (let poznamka of poznamky) {
    generator(poznamka["autor"], poznamka["datum"], poznamka["msg"])
}
