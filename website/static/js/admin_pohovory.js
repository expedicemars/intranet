let start_time = document.getElementById("start_time")
let end_time = document.getElementById("end_time")
let date = document.getElementById("date")



function seznam_casu() {
    let hodiny = ["7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"]
    let minuty = ["00", "20", "40"]
    for (let h of hodiny) {
        for (let m of minuty) {
            let opt = document.createElement("option")
            let value = h + ":" + m
            opt.value = value
            opt.innerHTML = value
            start_time.appendChild(opt.cloneNode(true))
            end_time.appendChild(opt.cloneNode(true))
        }
    }
}

seznam_casu()

