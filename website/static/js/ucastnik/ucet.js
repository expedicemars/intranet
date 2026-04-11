import httpGet from "../httpGet.js"
let info = JSON.parse(httpGet("/user_api/info"))
let confirmed = JSON.parse(httpGet("/user_api/confirmed"))["confirmation_status"]
let uzamcene_zmeny_udaju = JSON.parse(httpGet("/user_api/uzamcene_zmeny_udaju"))["status"]
let ids_list = ["jmeno", "prijmeni", "email", "adresa", "telcislo", "datum_narozeni", "rok_maturity", "zeme_puvodu", "mail_rodicu", "telcislo_rodicu", "tricko", "dozvedeli", "alergie", "skola", "osloveni_1p", "osloveni_5p", "zajmeno"]
let fixni_info_ids_list = ["confirmed", "odbornost", "progress", "datum_registrace", "datum_motivaku", "datum_shrnuti", "datum_prezentace", "datum_motivacniho_callu", "dalsi_kroky"]
let show_img_input_button = document.getElementById("show_img_input")
let img = document.getElementById("img_file");
let not_confirmed_div = document.getElementById("not_confirmed_div")
let confirmed_div = document.getElementById("confirmed_div")


if (uzamcene_zmeny_udaju) {
    for (let id of ids_list) {
        document.getElementById(id).disabled = "disabled"
    }
} else {
    show_img_input_button.addEventListener("click", function() {
        document.getElementById("img_input_div").hidden = false
    })
    img.addEventListener("change", function() {
        if(this.files[0].size > 5*1024*1024){
            alert("Nahraj prosím  menší obrázek, limit je 5MB");
            this.value = "";
        };
    })
}

// ovládá viditelnost divu co žádá o e-mail
if (confirmed) {
    not_confirmed_div.hidden = true
    confirmed_div.hidden = false
} else {
    not_confirmed_div.hidden = false
    confirmed_div.hidden = true
}



function nacist() {
    for (let id of ids_list) {
        document.getElementById(id).value = info[id]
    }
    for (let id of fixni_info_ids_list) {
        document.getElementById(id).innerHTML = info[id]
    }
}


// při změně formuláře to ukáže butonítka na uložení změn
function toggle_visibility_ulozit_buttonu() {
    document.getElementById("ulozit_1").hidden = false
    document.getElementById("ulozit_2").hidden = false
}

for (let id of ids_list) {
    document.getElementById(id).addEventListener("input", toggle_visibility_ulozit_buttonu)
}

nacist()
