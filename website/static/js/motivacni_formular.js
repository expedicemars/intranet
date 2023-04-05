import httpGet from "./httpGet.js"
let otazky = JSON.parse(httpGet("/user_api/motivacni_formular_otazky"))
let content_div = document.getElementById("content")

for (let o of otazky) {
    let h = document.createElement("h3")
    h.innerText = o["nadpis"]
    let p = document.createElement("p")
    p.innerText = o["popis"]
    let t = document.createElement("textarea")
    t.classList.add("form-control")
    t.name = o["name"]
    t.rows = 4
    let br = document.createElement("br")
    content_div.appendChild(h)
    content_div.appendChild(p)
    content_div.appendChild(t)
    content_div.appendChild(br)
}