import httpGet from "../httpGet.js"
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let content_div = document.getElementById("content")

// zadani

for (let odbornost of dostupne_odbornosti) {
    let div = document.createElement("div")
    div.classList.add("rounded-2", "border-orange", odbornost.system_name+"-div", "my-2", "p-2")
    content_div.appendChild(div)

    let h3 = document.createElement("h3")
    h3.innerText = "Zadání pro " + odbornost.ctvrtypmc
    div.appendChild(h3)

    let r1 = document.createElement("row")
    r1.classList.add("row")
    div.appendChild(r1)
    let c1 = document.createElement("div")
    c1.classList.add("col")
    r1.appendChild(c1)
    let c2 = document.createElement("div")
    c2.classList.add("col-auto")
    r1.appendChild(c2)


    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost.system_name))
    if (zadani.length != 0) {
        for (let filename of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost.system_name + "/" + filename
            a.download = filename
            a.innerHTML = filename
            a.classList.add("link")
            c1.appendChild(a)
            c1.appendChild(document.createElement("br"))
        }
    } else {
        c1.innerText = "Bohužel, tvoje odbornost ještě žádný zadání neuploadla. Měli by to udělat co nejdřív!"
    }

    
    let a = document.createElement("a")
    a.href = "/odbornost/" + odbornost.system_name
    c2.appendChild(a)

    let button = document.createElement("button")
    button.classList.add("btn", "em-button")
    button.type = button
    button.innerText = "Detail"
    a.appendChild(button)



}