let generovat_button = document.getElementById("generovat")
let jakakoli = document.getElementById("jakakoli")
let jakykoli = document.getElementById("jakykoli")
let nezalezi = document.getElementById("nezalezi")





generovat_button.addEventListener("click", vyhodnotit)
jakakoli.addEventListener("change", function() {
    for (let id of ["biolog", "konstrukter", "fyzik", "inzenyr", "popularizator"]) {
        document.getElementById(id).checked = false
    }
})
jakykoli.addEventListener("change", function() {
    for (let id of ["Domácí kolo", "Semifinále", "Finále", "Simulace"]) {
        document.getElementById(id).checked = false
    }
})



function vyhodnotit() {
    let result = {}
    // odbornost
    if (jakakoli.checked) {
        result["odbornost"] = "jakakoli"
    } else {
        let res = []
        for (let odb of ["biolog", "konstrukter", "fyzik", "inzenyr", "popularizator"]) {
            if (document.getElementById(odb).checked) {
                res.push(odb)
            }
        }
        result["odbornost"] = res
    }

    // postup
    if (jakykoli.checked) {
        result["postup"] = "jakykoli"
    } else {
        let res = []
        for (let pos of ["Domácí kolo", "Semifinále", "Finále", "Simulace"]) {
            if (document.getElementById(pos).checked) {
                res.push(pos)
            }
        }
        result["postup"] = res
    }

    // chybejici udaj
    result["udaj"] = ""
    if (nezalezi.checked) {
        result["udaj"] = "nezalezi"
    } else {
        for (let udaj of ["jmeno", "telcislo", "adresa", "mail_rodicu", "odbornost", "datum_narozeni", "tricko", "dozvedeli", "skola", "alergie", "motivak", "prace", "profilovka"]) {
            if (document.getElementById(udaj).checked) {
                result["udaj"] = udaj
                break
            }
        }
    }

    // vypsat

    let res = []
    for (let id of ["prazdny_vypsat", "jmeno_vypsat", "email_vypsat", "telcislo_vypsat", "adresa_vypsat", "mail_rodicu_vypsat", "odbornost_vypsat", "progress_vypsat", "datum_narozeni_vypsat", "tricko_vypsat", "dozvedeli_vypsat", "alergie_vypsat", "skola_vypsat", "admin_poznamka_vypsat", "hodnoceni_vypsat"]) {
        if (document.getElementById(id).checked) {
            res.push(id)
        }
    }
    result["vypsat"] = res

    // kontrola
    if (result["odbornost"].length == 0) {
        alert("nevybral jsi žádnou odbornost.")
    } else if (result["postup"].length == 0) {
        alert("nevybral jsi žádný postup.")
    } else if (result["udaj"].length == 0) {
        alert("nezadal jsi žádné info o chybějících údajích.")
    } else {
        if (result["vypsat"].length == 0) {
            result["vypsat"] = ["prazdny_vypsat"]
        }
        document.getElementById("result").value = JSON.stringify(result)
        document.getElementById("form").submit()
    }

}
