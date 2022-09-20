import httpGet from "./httpGet.js"
let existuje = JSON.parse(httpGet("/send_admin/prohlaseni_rodicu_existuje"))
let existuje_div = document.getElementById("existuje")

if (existuje["existuje"]) {
    let a = document.createElement("a")
    a.innerHTML = "Stáhnout současnou verzi"
    a.href = "/send_user/prohlaseni_rodicu"
    a.download = "prohlaseni_rodicu.docx"
    existuje_div.appendChild(a)
} else {
    existuje_div.innerHTML = "Žádné prohlášení tu ještě nahrané není."
}