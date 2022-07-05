import httpGet from "./httpGet.js"
let terminy = JSON.parse(httpGet("/send_user/terminy"))
let terminy_div = document.getElementById("terminy")
let result_input = document.getElementById("result")
let form = document.getElementById("form")
let registrace_date = document.getElementById("registrace_date")
let registrace_time = document.getElementById("registrace_time")

document.getElementById("novy_termin").addEventListener("click", function() {novy_zaznam("", null, null)})
document.getElementById("ulozit").addEventListener("click", vyhodnotit)



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

    let r2c5 = document.createElement("div")
    r2c5.classList.add("col")
    row2.appendChild(r2c5)

    let smazat_btn = document.createElement("button")
    smazat_btn.classList.add("btn", "btn-danger")
    smazat_btn.type="button"
    smazat_btn.innerHTML = "Smazat Termín"
    r2c5.appendChild(smazat_btn)
    smazat_btn.addEventListener("click", function() {
        smazat_btn.parentElement.parentElement.parentElement.remove()
    })


}


for (let zaznam of terminy) {
    // zaznam "registrace" je spešl
    if (zaznam["popis"] == "registrace") {
        registrace_date.value = zaznam["date"]
        registrace_time.value = zaznam["time"]
    } else {
        novy_zaznam(zaznam["popis"], zaznam["date"], zaznam["time"])
    }
}


function vyhodnotit() {
    let result = []
    for (let div of terminy_div.childNodes) {
        let zaznam = {}
        zaznam["popis"] = div.childNodes[0].childNodes[1].childNodes[0].value
        zaznam["date"] = div.childNodes[1].childNodes[1].childNodes[0].value
        zaznam["time"] = div.childNodes[1].childNodes[3].childNodes[0].value

        result.push(zaznam)
    }
    // zaznam o registraci
    let zaznam_o_registraci = {}
    zaznam_o_registraci["popis"] = "registrace"
    zaznam_o_registraci["date"] = registrace_date.value
    zaznam_o_registraci["time"] = registrace_time.value

    result.push(zaznam_o_registraci)
    result_input.value = JSON.stringify(result)
    form.submit()
}