import httpGet from "./httpGet.js"
let emaily = httpGet("/admin_api/emaily_admin_editoru")
let odkazy = JSON.parse(httpGet("/admin_api/odkazy"))
let odkazy_list = document.getElementById("odkazy")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let tbody = document.getElementById("tbody")
let statistiky = JSON.parse(httpGet("/admin_api/statistiky"))

document.getElementById("emails").innerHTML = emaily

for (let o of odkazy) {
    let li = document.createElement("li")
    odkazy_list.appendChild(li)
    let a = document.createElement("a")
    li.appendChild(a)
    a.innerHTML = o["popis"]
    a.href = o["odkaz"]
    a.target = "_blank"
    a.classList.add("link")
}

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
console.log(statistiky)


for (let key of Object.keys(statistiky)) {
    document.getElementById(key).innerText = statistiky[key]
}

