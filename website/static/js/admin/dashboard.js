import httpGet from "../httpGet.js"
let emaily = httpGet("/admin_api/emaily_admin_editoru")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let tbody = document.getElementById("tbody")
let statistiky = JSON.parse(httpGet("/admin_api/statistiky"))

document.getElementById("emails").innerHTML = emaily

// vemu si children, appendnu neco doprostred a vratim je tam
let children = Array.from(tbody.children)
for (let odbornost of dostupne_odbornosti) {
    let tr = document.createElement("tr")
    let th = document.createElement("td")
    th.innerText = odbornost.druhypmc
    tr.appendChild(th)
    let td = document.createElement("td")
    td.id = odbornost.system_name
    tr.appendChild(td)
    children.splice(-4, 0, tr)
}
tbody.innerHTML = null
for (let ch of children) {
    tbody.appendChild(ch)
}


for (let key of Object.keys(statistiky)) {
    document.getElementById(key).innerText = statistiky[key]
}

