import httpGet from "./httpGet.js"
let existuje = JSON.parse(httpGet("/admin_api/prohlaseni_rodicu_existuje"))
let prohlaseni_link_div = document.getElementById("prohlaseni_link")

if (existuje["existuje"]) {
    let a = document.createElement("a")
    a.innerHTML = "Stáhnout současnou verzi"
    a.href = "/file_api/prohlaseni_rodicu"
    a.download = "prohlaseni_rodicu.docx"
    prohlaseni_link_div.appendChild(a)
    a.classList.add("link")
} else {
    prohlaseni_link_div.innerHTML = "Žádné prohlášení tu ještě nahrané není."
}