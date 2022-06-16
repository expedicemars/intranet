import httpGet from "./httpGet.js"
let role_uzivatele = JSON.parse(httpGet("/send_admin/role_" + parseInt(document.getElementById("id").value)))
let seznam_omezeni = JSON.parse(httpGet("/send_admin/vsechny_omezeni"))
let checkdiv = document.getElementById("check")
let btn = document.getElementById("btn")
let resut_input = document.getElementById("result")
let form = document.getElementById("form")

btn.addEventListener("click", vyhodnotit)



function generator_checkeru(label, is_checked) {
    let inp = document.createElement("input")
    inp.classList.add("form-check-input")
    inp.type="checkbox"
    inp.checked = is_checked
    inp.id = label

    let lab = document.createElement("label")
    lab.classList.add("form-check-label")
    lab.for = label
    lab.innerHTML = label

    let di = document.createElement("div")
    di.classList.add("form-check")
    di.appendChild(inp)
    di.appendChild(lab)
    return di

}

for (let label of seznam_omezeni) {
    let is_checked = role_uzivatele.includes(label)
    checkdiv.appendChild(generator_checkeru(label, is_checked))
}

function vyhodnotit() {
    let result = []
    for (let child of checkdiv.childNodes) {
        let inp = child.childNodes[0]
        if (inp.checked) {
            result.push(inp.id)
        }
    }
    resut_input.value = JSON.stringify(result)
    form.submit()
}
