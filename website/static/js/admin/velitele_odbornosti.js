import httpGet from "../httpGet.js"
let odbornosti_kterym_velim = JSON.parse(httpGet("/admin_api/odbornosti_kterym_velim"))
let data = JSON.parse(httpGet("/admin_api/velitel_odbornosti_data"))
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let content_div = document.getElementById("content")

for (let odbornost of odbornosti_kterym_velim) {
    let div = document.createElement("div")
    div.classList.add("border-orange", "rounded-2", "m-2", "p-2", "lighter")
    content_div.appendChild(div)
    
    let h2 = document.createElement("h2")
    for (let odb_data of dostupne_odbornosti) {
        if (odb_data["system_name"] == odbornost) {
            h2.innerText = odb_data["prvnipmc"]
        }
    }
    div.appendChild(h2)

    let nahrat_zadani_div = document.createElement("div")
    let ukazat_zadani_div = document.createElement("div")
    let kontakt_div = document.createElement("div")
    div.appendChild(nahrat_zadani_div)
    div.appendChild(ukazat_zadani_div)
    div.appendChild(document.createElement("hr"))
    div.appendChild(kontakt_div)

    let p1 = document.createElement("p")
    p1.innerText = "Přidej soubory zadání, pokud jich je víc, tak všechny naráz:"
    nahrat_zadani_div.appendChild(p1)
    let r1 = document.createElement("row")
    r1.classList.add("row")
    nahrat_zadani_div.appendChild(r1)
    let c1 = document.createElement("div")
    c1.classList.add("col")
    r1.appendChild(c1)
    let c2 = document.createElement("div")
    c2.classList.add("col-auto")
    r1.appendChild(c2)

    let file_input = document.createElement("input")
    file_input.type = "file"
    file_input.multiple = true
    file_input.classList.add("form-control", "my-2")
    file_input.name = odbornost + "_files"
    c1.appendChild(file_input)

    let file_button = document.createElement("button")
    file_button.type = "submit"
    file_button.name = "ulozit_zadani"
    file_button.value = odbornost
    file_button.classList.add("btn", "btn-outline-success")
    file_button.innerText = "Nahrát"
    c2.appendChild(file_button)
    
    let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost))
    if (zadani.length != 0) {
        nahrat_zadani_div.hidden = true
        ukazat_zadani_div.hidden = false

        let smazat_button = document.createElement("button")
        smazat_button.type = "submit"
        smazat_button.classList.add("btn", "btn-danger")
        smazat_button.name = "smazat_zadani"
        smazat_button.value = odbornost
        smazat_button.innerText = "Smazat zadání"
        ukazat_zadani_div.appendChild(smazat_button)

        ukazat_zadani_div.appendChild(document.createElement("br"))

        for (let zadani_file of zadani) {
            let a = document.createElement("a")
            a.href = "/file_api/zadani_file/"+ odbornost + "/" + zadani_file
            a.download = zadani_file
            a.innerHTML = zadani_file
            a.classList.add("link")
            ukazat_zadani_div.appendChild(a)
            ukazat_zadani_div.appendChild(document.createElement("br"))
        }
    } else {
        let p2 = document.createElement("p")
        p2.innerText = "Ještě tu žádné zadání nahrané není."
        nahrat_zadani_div.appendChild(p2)
        nahrat_zadani_div.hidden = false
        ukazat_zadani_div.hidden = true
    }

    let p3 = document.createElement("p")
    p3.innerText = "Sem napiš nějaké možnosti kontaktu. Třeba jméno, email, další jméno, jeho email..."
    kontakt_div.appendChild(p3)

    let r2 = document.createElement("row")
    r2.classList.add("row")
    kontakt_div.appendChild(r2)
    let c3 = document.createElement("div")
    c3.classList.add("col")
    r2.appendChild(c3)
    let c4 = document.createElement("div")
    c4.classList.add("col-auto")
    r2.appendChild(c4)

    let kontakt_input = document.createElement("input")
    kontakt_input.type = "text"
    kontakt_input.classList.add("form-control")
    kontakt_input.name = odbornost
    kontakt_input.id = odbornost
    kontakt_input.value = data[odbornost]
    c3.appendChild(kontakt_input)

    let ulozit_button = document.createElement("button")
    ulozit_button.type = "submit"
    ulozit_button.classList.add("btn", "btn-outline-success")
    ulozit_button.name = "ulozit_kontakt"
    ulozit_button.value = odbornost
    ulozit_button.innerText = "Uložit kontakt"
    c4.appendChild(ulozit_button)

    
}