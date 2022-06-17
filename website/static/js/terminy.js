import httpGet from "./httpGet.js"
let terminy = JSON.parse(httpGet("/send_user/terminy"))
let terminy_div = document.getElementById("terminy")

for (let zaznam of terminy) {
    novy_zaznam(zaznam["popis"], zaznam["date"], zaznam["time"])
}


function novy_zaznam(popis, date, time) {
    let div = document.createElement("div")
    div.classList.add("border", "rounded-2", "border-secondary", "m-2", "p-2")
    terminy_div.appendChild(div)

    let row1 = document.createElement("div")
    row1.classList.add("row", "m-1")
    div.appendChild(row1)

    let r1c1 = document.createElement("div")
    r1c1.classList.add("col-auto")
    r1c1.innerHTML = "Popis: "
    row1.appendChild(r1c1)

    let r1c2 = document.createElement("div")
    r1c2.classList.add("col")
    row1.appendChild(r1c2)

    let inp = document.createElement("input")
    inp.type="text"
    inp.classList.add("form-control")
    inp.value=popis
    r1c2.appendChild(inp)
    inp.disabled = true

    let row2 = document.createElement("div")
    row2.classList.add("row", "m-1")
    div.appendChild(row2)

    let r2c1 = document.createElement("div")
    r2c1.classList.add("col-auto")
    r2c1.innerHTML = "Datum: "
    row2.appendChild(r2c1)

    let r2c2 = document.createElement("div")
    r2c2.classList.add("col")
    row2.appendChild(r2c2)

    let date_inp = document.createElement("input")
    date_inp.type="date"
    date_inp.value=date
    r2c2.appendChild(date_inp)
    date_inp.disabled = true

    let r2c3 = document.createElement("div")
    r2c3.classList.add("col-auto")
    r2c3.innerHTML = "Čas: "
    row2.appendChild(r2c3)

    let r2c4 = document.createElement("div")
    r2c4.classList.add("col")
    row2.appendChild(r2c4)
    
    let time_inp = document.createElement("input")
    time_inp.type="time"
    time_inp.value=time
    r2c4.appendChild(time_inp)
    time_inp.disabled = true
}
