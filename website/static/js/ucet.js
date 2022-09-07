import httpGet from "./httpGet.js"
let info = JSON.parse(httpGet("/send_user/info"))
let zmeny_button = document.getElementById("zmeny")
let form = document.getElementById("form")
let ids_list = ["jmeno", "email", "adresa", "telcislo", "datum_narozeni", "mail_rodicu"]
let fixni_info_ids_list = ["confirmed", "souhlas_rodicu", "odbornost", "progress"]
let show_img_input_button = document.getElementById("show_img_input")
let img = document.getElementById("img_file");
let je_motivak_nahrany = httpGet("/send_user/je_motivak_nahrany")
let motivak_div = document.getElementById("nahrany_motivak")



zmeny_button.addEventListener("click", toggle_zmeny)
show_img_input_button.addEventListener("click", function() {
    document.getElementById("img_input_div").hidden = false
})
img.addEventListener("change", function() {
    if(this.files[0].size > 1000000){
       alert("Nahraj prosím  menší obrázek, limit je 1MB");
       this.value = "";
    };
})
console.log(je_motivak_nahrany)
if (je_motivak_nahrany != "no") {
    motivak_div.hidden = false
    let a = document.createElement("a")
    motivak_div.appendChild(a)
    a.href = "/send_user/motivak"
    a.innerHTML = "Stáhnout stávající verzi motiváku"
    a.download = ""
}



function nacist() {
    for (let id of ids_list) {
        document.getElementById(id).value = info[id]
    }
    //nacteni tricka
    let preselected_id = ""
    if (info["tricko"]) {
        preselected_id = info["tricko"]
    } else { // bude vyuzito jen poprve, kdyz je user zalozenej
        preselected_id = "nic"
    }
    document.getElementById(preselected_id).selected = "selected"
    //nacteni fixnich
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
        document.getElementById("tricko_select").disabled = true
        odeslat_formular()
    } else {
        zmeny_button.value = "upravy"
        zmeny_button.innerHTML = "Uložit změny"
        for (let id of ids_list) {
            document.getElementById(id).disabled = false
        }  
        document.getElementById("tricko_select").disabled = false
    }
}


function odeslat_formular() {
    let result = {}
    for (let id of ids_list) {
        result[id] = document.getElementById(id).value
    }
    result["tricko"] = document.getElementById("tricko_select").value
    document.getElementById("result").value = JSON.stringify(result)
    form.submit()
}

nacist()