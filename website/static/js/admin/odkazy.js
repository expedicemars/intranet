import httpGet from "../httpGet.js"
import TableCreator from "../table_creator.js";


let content_div = document.getElementById("content")
let odkazy = JSON.parse(httpGet("/admin_api/odkazy"))
let pridat_button = document.getElementById("pridat_button")
let select = document.getElementById("select")

pridat_button.addEventListener("click", function() {
    if (select.value == "vybrat") {
        alert("Nebyla vybrána žádná kategorie.")
    } else {
        let nazvy = [] // protoze jsem lazy  a nazev je UID
        odkazy.forEach(kategorie => {
            kategorie.odkazy.forEach(radek => {
                nazvy.push(radek.nazev)
            })
        })
        if (nazvy.includes(document.getElementById("nazev").value)) {
            alert("Zvolený název linku už existuje. Zvol prosím jiný text linku.")
        } else {
            document.getElementById("form").submit()
        }
    }
})

odkazy.forEach(kategorie => {
    let opt = document.createElement("option")
    opt.innerText = kategorie.display_name
    opt.value = kategorie.system_name
    select.appendChild(opt)
})

odkazy.forEach(kategorie => {
    // nadpis
    let h2 = document.createElement("h2")
    h2.innerText = kategorie.display_name
    content_div.appendChild(h2)

    let parent_div = document.createElement("div")
    content_div.append(parent_div)

    // tabulka
    let t = new TableCreator(parent_div)

    kategorie.odkazy.forEach(radek => {
        let a = document.createElement("a")
        a.innerText = radek.nazev
        a.href = radek.adresa
        a.classList.add("link")
        a.target = "_blank"

        let b = document.createElement("button")
        b.classList.add("btn", "btn-danger")
        b.type = "button"
        b.innerHTML = "Smazat"
        b.addEventListener("click", function() {
            document.getElementById("name_to_delete").value = radek.nazev
            document.getElementById("result").submit()
        })

        t.make_row([a, b], [0, 0])
    });
});