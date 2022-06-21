import httpGet from "./httpGet.js"
let info = JSON.parse(httpGet("/send_user/info"))
let zmeny_button = document.getElementById("zmeny")
let form = document.getElementById("form")
let ids_list = ["jmeno", "email", "adresa", "telcislo", "datum_narozeni", "mail_rodicu"]
let fixni_info_ids_list = ["confirmed", "souhlas_rodicu", "odbornost", "progress"]
let show_img_input_button = document.getElementById("show_img_input")

zmeny_button.addEventListener("click", toggle_zmeny)
show_img_input_button.addEventListener("click", function() {
    document.getElementById("img_input_div").hidden = false
})


function nacist() {
    for (let id of ids_list) {
        document.getElementById(id).value = info[id]
    }
    for (let id of fixni_info_ids_list) {
        document.getElementById(id).innerHTML = info[id]
    }
}


function toggle_zmeny() {
    if (zmeny_button.value == "upravy") {
        zmeny_button.value = "zamknuto"
        zmeny_button.innerHTML = "Odemknout úpravy"
        for (let id of ids_list) {
            document.getElementById(id).disabled = true
        }
        odeslat_formular()
    } else {
        zmeny_button.value = "upravy"
        zmeny_button.innerHTML = "Uložit změny"
        for (let id of ids_list) {
            document.getElementById(id).disabled = false
        }
    }
}


function odeslat_formular() {
    let result = {}
    for (let id of ids_list) {
        result[id] = document.getElementById(id).value
    }
    document.getElementById("result").value = JSON.stringify(result)
    form.submit()
}

nacist()