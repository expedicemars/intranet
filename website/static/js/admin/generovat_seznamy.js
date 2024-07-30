import httpGet from "../httpGet.js"

let generovat_button = document.getElementById("generovat")
let jakakoli = document.getElementById("jakakoli")
let bez_odbornosti = document.getElementById("bez_odbornosti")
let jakykoli = document.getElementById("jakykoli")
let nezalezi_ma = document.getElementById("nezalezi_ma")
let nezalezi_nema = document.getElementById("nezalezi_nema")
let jakakoli_uzamcenost = document.getElementById("uzamcene_zmeny_cokoli")
let vyber_div = document.getElementById("vyber")
let vysledek_div = document.getElementById("vysledek")
let ukazat_button = document.getElementById("ukazat")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let dostupne_progressy = JSON.parse(httpGet("/noauth_api/dostupne_progressy"))
let odbornosti_inputs = document.getElementById("odbornosti")
let progressy_inputs = document.getElementById("progressy")
let udaje_ma_inputs = document.getElementById("udaje_ma")
let udaje_nema_inputs = document.getElementById("udaje_nema")
let novy_sloupecek_button = document.getElementById("novy_sloupecek")
let vypsat_selects_div = document.getElementById("vypsat_selects")

// id, mail, confirmed, password, odbornost, progress, role, admin_poznamka, datum_registrace, nema cenu filtrovat?
let udaje_k_filtrovani = [
    {
        "system_name": "jmeno",
        "display_name": "Jméno",
    },
    {
        "system_name": "prijmeni",
        "display_name": "Příjmení",
    },
    {
        "system_name": "adresa",
        "display_name": "Adresa",
    },
    {
        "system_name": "telcislo",
        "display_name": "Telefonní číslo",
    },
    {
        "system_name": "mail_rodicu",
        "display_name": "E-mail rodičů",
    },
    {
        "system_name": "datum_narozeni",
        "display_name": "Datum narození",
    },
    {
        "system_name": "tricko",
        "display_name": "Tričko",
    },
    {
        "system_name": "dozvedeli",
        "display_name": "Jak se o EM dozvěděli",
    },
    {
        "system_name": "alergie",
        "display_name": "Alergie",
    },
    {
        "system_name": "skola",
        "display_name": "Škola",
    },
    {
        "system_name": "datum_motivacniho_callu",
        "display_name": "Datum motivačního callu",
    },
    {
        "system_name": "meeting_link",
        "display_name": "Odkaz na call",
    },
    {
        "system_name": "hodnoceni",
        "display_name": "Hodnocení po callu"
    },
    {
        "system_name": "osloveni_1p",
        "display_name": "Oslovení (1. pád)",
    },
    {
        "system_name": "osloveni_5p",
        "display_name": "Oslovení (5. pád)",
    },
    {
        "system_name": "zajmeno",
        "display_name": "Zájmeno",
    },
    {
        "system_name": "profilovka",
        "display_name": "Profilová fotka",
    }
]

// password, role nema cenu vypisovat
let udaje_k_vypsani = [
    {
        "system_name": "prazdny",
        "display_name": "Prázdný sloupeček"
    },
    {
        "system_name": "id",
        "display_name": "Id"
    },
    {
        "system_name": "email",
        "display_name": "E-mail"
    },
    {
        "system_name": "confirmed",
        "display_name": "Ověřený mail"
    },
    {
        "system_name": "jmeno",
        "display_name": "Jméno",
    },
    {
        "system_name": "prijmeni",
        "display_name": "Příjmení",
    },
    {
        "system_name": "adresa",
        "display_name": "Adresa",
    },
    {
        "system_name": "telcislo",
        "display_name": "Telefonní číslo",
    },
    {
        "system_name": "mail_rodicu",
        "display_name": "E-mail rodičů",
    },
    {
        "system_name": "odbornost",
        "display_name": "Odbornost"
    },
    {
        "system_name": "datum_narozeni",
        "display_name": "Datum narození",
    },
    {
        "system_name": "progress",
        "display_name": "Postup v Expedici"
    },
    {
        "system_name": "tricko",
        "display_name": "Tričko",
    },
    {
        "system_name": "dozvedeli",
        "display_name": "Jak se o EM dozvěděli",
    },
    {
        "system_name": "admin_poznamka",
        "display_name": "Admin poznámka"
    },
    {
        "system_name": "uzamcene_zmeny_callu",
        "display_name": "Uzamčené změny callů"
    },
    {
        "system_name": "uzamcene_zmeny_prace",
        "display_name": "Uzamčené změny práce"
    },
    {
        "system_name": "uzamcene_zmeny_udaju",
        "display_name": "Uzamčené změny údajů"
    },
    {
        "system_name": "alergie",
        "display_name": "Alergie",
    },
    {
        "system_name": "skola",
        "display_name": "Škola",
    },
    {
        "system_name": "datum_registrace",
        "display_name": "Datum registrace"
    },
    {
        "system_name": "datum_motivacniho_callu",
        "display_name": "Datum motivačního callu",
    },
    {
        "system_name": "meeting_link",
        "display_name": "Odkaz na call",
    },
    {
        "system_name": "odevzdany_motivacni_dotaznik",
        "display_name": "Odevzdaný motivační dotazník"
    },
    {
        "system_name": "osloveni_1p",
        "display_name": "Oslovení (1. pád)",
    },
    {
        "system_name": "osloveni_5p",
        "display_name": "Oslovení (5. pád)",
    },
    {
        "system_name": "zajmeno",
        "display_name": "Zájmeno",
    }
]


// vygenerování inputů podle dostupných odborností a progressů
for (let odb of dostupne_odbornosti) {
    let inp = document.createElement("input")
    inp.type = "checkbox"
    inp.name = "odbornost"
    inp.id = odb.system_name
    inp.addEventListener("change", function() {
        jakakoli.checked = false
        bez_odbornosti.checked = false
    })

    let lab = document.createElement("label")
    lab.htmlFor = odb.system_name
    lab.innerText = odb.prvnipjc

    odbornosti_inputs.appendChild(document.createElement("br"))
    odbornosti_inputs.appendChild(inp)
    odbornosti_inputs.append(lab)
}

for (let d of dostupne_progressy) {
    let inp = document.createElement("input")
    inp.type = "checkbox"
    inp.name = "postup"
    inp.id = d
    inp.addEventListener("change", function() {
        jakykoli.checked = false
    })

    let lab = document.createElement("label")
    lab.htmlFor = d
    lab.innerText = d

    progressy_inputs.appendChild(document.createElement("br"))
    progressy_inputs.appendChild(inp)
    progressy_inputs.append(lab)
}

for (let u of udaje_k_filtrovani) {
    let inp_ma = document.createElement("input")
    inp_ma.type = "radio"
    inp_ma.name = "udaje_ma"
    inp_ma.id = u["system_name"] + "_ma"

    let lab_ma = document.createElement("label")
    lab_ma.htmlFor = u["system_name"] + "_ma"
    lab_ma.innerText = u["display_name"]

    udaje_ma_inputs.appendChild(document.createElement("br"))
    udaje_ma_inputs.appendChild(inp_ma)
    udaje_ma_inputs.append(lab_ma)

    let inp_nema = document.createElement("input")
    inp_nema.type = "radio"
    inp_nema.name = "udaje_nema"
    inp_nema.id = u["system_name"] + "_nema"

    let lab_nema = document.createElement("label")
    lab_nema.htmlFor = u["system_name"] + "_nema"
    lab_nema.innerText = u["display_name"]

    udaje_nema_inputs.appendChild(document.createElement("br"))
    udaje_nema_inputs.appendChild(inp_nema)
    udaje_nema_inputs.append(lab_nema)
}

// generovani novych sloupecku

function novy_sloupecek() {
    let row = document.createElement("div")
    row.classList.add("row", "my-1")
    let c1 = document.createElement("div")
    c1.classList.add("col-sm")
    let c2 = document.createElement("div")
    c2.classList.add("col-auto")
    let select = document.createElement("select")
    select.classList.add("form-select")
    let smazat_button = document.createElement("button")
    smazat_button.classList.add("btn", "btn-danger")
    smazat_button.type = "button"
    smazat_button.innerText = "Odebrat sloupeček"
    smazat_button.addEventListener("click", function() {
        row.remove()
    })

    vypsat_selects_div.appendChild(row)
    row.appendChild(c1)
    row.appendChild(c2)
    c1.appendChild(select)
    c2.appendChild(smazat_button)

    for (let u of udaje_k_vypsani) {
        let opt = document.createElement("option")
        opt.value = u.system_name
        opt.innerText = u.display_name
        select.appendChild(opt)
    }
}

// vyhodnotit - pouzita v jednom event listeneru

function vyhodnotit() {
    let result = {}

    // odbornost
    if (jakakoli.checked) {
        result["odbornost"] = "jakakoli"
    } else if (bez_odbornosti.checked) {
        result["odbornost"] = "bez_odbornosti"
    } else {
        let res = []
        for (let odb of dostupne_odbornosti) {
            if (document.getElementById(odb.system_name).checked) {
                res.push(odb.system_name)
            }
        }
        result["odbornost"] = res
    }

    // postup
    if (jakykoli.checked) {
        result["postup"] = "jakykoli"
    } else {
        let res = []
        for (let pos of dostupne_progressy) {
            if (document.getElementById(pos).checked) {
                res.push(pos)
            }
        }
        result["postup"] = res
    }

    // maji udaj
    result["udaj_ma"] = ""
    if (nezalezi_ma.checked) {
        result["udaj_ma"] = "nezalezi"
    } else {
        for (let udaj of udaje_k_filtrovani) {
            if (document.getElementById(udaj.system_name + "_ma").checked) {
                result["udaj_ma"] = udaj["system_name"]
                break
            }
        }
    }

    // chybejici udaj
    result["udaj_nema"] = ""
    if (nezalezi_nema.checked) {
        result["udaj_nema"] = "nezalezi"
    } else {
        for (let udaj of udaje_k_filtrovani) {
            if (document.getElementById(udaj.system_name + "_nema").checked) {
                result["udaj_nema"] = udaj["system_name"]
                break
            }
        }
    }

    // uzamčenost změn

    if (jakakoli_uzamcenost.checked) {
        result["uzamcenost_zmen"] = "jakakoli"
    } else {
        result["uzamcenost_zmen"] = []
        for (let id of ["uzamcene_zmeny_callu", "uzamcene_zmeny_prace", "uzamcene_zmeny_udaju"]) {
            if (document.getElementById(id).checked) {
                result["uzamcenost_zmen"].push(id)
            }
        }
    }

    // odevzdany motivak

    let radios_m = document.getElementsByName("odevzdany_dotaznik")
    for (let r of radios_m) {
        if (r.checked) {
            result["odevzdany_dotaznik"] = r.value
        }
    }

    // vypsat
    let res = []
    for (let ch of vypsat_selects_div.children) {
        let select_node = ch.children[0].children[0]
        res.push(select_node.value)
    }
    result["vypsat"] = res

    // kontrola
    if (result["odbornost"].length == 0) {
        alert("nevybral jsi žádnou odbornost.")
    } else if (result["postup"].length == 0) {
        alert("nevybral jsi žádný postup.")
    } else  if (result["vypsat"].length == 0){
        alert("Nebyl určen žádný sloupeček, ktereý chceš k vybraným účastníkům vypsat.")
    } else {
        vyber_div.hidden = true
        generovat_button.hidden = true
        vysledek_div.hidden = false
        ukazat_button.hidden = false
        $.ajax({
            data : {
                result: JSON.stringify(result)
            },
            type: "POST",
            url: "/admin/generovat_seznamy"
        })
        .done(function(data) {
            vypsat(data)
        })
    }

}
// funkce na to vypisování, volaná z ajaxu z funkce vyhodnotit
function vypsat(data) {
    data = JSON.parse(data)
    document.getElementById("emaily_vybranych").innerHTML = data["emails"].join(", ")
    let tr = document.getElementById("tr")
    let tbody = document.getElementById("tbody")
    // smazani stare tabulky
    while (tr.firstChild) {
        tr.removeChild(tr.firstChild)
    }
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild)
    }
    // nadpisy
    let th = document.createElement("th")
    th.innerText = "Účet"
    tr.appendChild(th)
    for (let key of data["keys"]) {
        let th = document.createElement("th")
        for (let udaj of udaje_k_vypsani) {
            if (udaj["system_name"] == key) {
                th.innerText = udaj["display_name"]
                break
            }
        } 
        tr.appendChild(th)
    }
    // content
    for (let u of data["users"]) {
        let tr = document.createElement("tr")
        tr.classList.add("tr-min-height")
        tbody.append(tr)

        let td = document.createElement("td")
        tr.appendChild(td)

        let a = document.createElement("a")
        a.href = "/admin/detail_usera/" + u["id_na_link"]
        a.classList.add("link")
        a.innerText = "#"
        td.appendChild(a)
        
        for (let key of data["keys"]) {
            let td = document.createElement("td")
            td.innerText = u[key]
            tr.appendChild(td)
        }
    }
    
}


// event listeners

generovat_button.addEventListener("click", vyhodnotit)
novy_sloupecek_button.addEventListener("click", novy_sloupecek)

ukazat_button.addEventListener("click", function() {
    generovat_button.hidden = false
    vyber_div.hidden = false
    ukazat_button.hidden = true
})
jakakoli.addEventListener("change", function() {
    for (let odb of dostupne_odbornosti) {
        document.getElementById(odb["system_name"]).checked = false
    }
    bez_odbornosti.checked = false
})
bez_odbornosti.addEventListener("change", function() {
    for (let odb of dostupne_odbornosti) {
        document.getElementById(odb["system_name"]).checked = false
    }
    jakakoli.checked = false
})
jakykoli.addEventListener("change", function() {
    for (let id of dostupne_progressy) {
        document.getElementById(id).checked = false
    }
})
jakakoli_uzamcenost.addEventListener("change", function() {
    for (let radio of document.getElementsByName("uzamcenost_zmen")) {
        radio.checked = false
    }
})
for (let radio of document.getElementsByName("uzamcenost_zmen")) {
    radio.addEventListener("change", function() {
        jakakoli_uzamcenost.checked = false
    })
}
novy_sloupecek() // aby tam vzdy byl jeden