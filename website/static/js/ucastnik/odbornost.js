import httpGet from "../httpGet.js"
let odbornost = document.getElementById("odbornost").value
let kontakt = httpGet("/user_api/kontakt_na_velitele_odbornosti/" + odbornost)
let zadani = JSON.parse(httpGet("/file_api/filenames_vsech_zadani_v_odbornosti/" + odbornost))
let nahrane_shrnuti_input = document.getElementById("nahrane_shrnuti")
let nahrana_prace_input = document.getElementById("nahrana_prace")
let vzor = JSON.parse(httpGet("/user_api/vzorove_vypracovani_existuje"))
let vzor_span = document.getElementById("vzor")

document.getElementById("kontakt").innerText = kontakt

if (vzor.existuje) {
    vzor_span.innerHTML = "Vzorové vypracování najdeš <a  class='link' href='/file_api/vzorove_vypracovani'>tady</a>."
} else {
    vzor_span.innerText = "Vzorové vypracování ještě neexistuje, ale až ho vytvoříme, bude tady."
}

if (zadani.length != 0) {
    for (let zadani_file of zadani) {
        let a = document.createElement("a")
        a.classList.add("link")
        a.href = "/file_api/zadani_file/" + odbornost + "/" + zadani_file
        a.download = zadani_file
        a.innerHTML = zadani_file
        document.getElementById("zadani_single").appendChild(a)
        document.getElementById("zadani_single").appendChild(document.createElement("br"))
    }
} else {
    document.getElementById("zadani_single").innerHTML = "Bohužel, tvoje odbornost ještě žádný zadání nenahrála. Měli by to udělat co nejdřív!"
}

// shrnutí
let shrnuti = JSON.parse(httpGet("/file_api/send_filename_vlastniho_shrnuti"))
let ukazat_shrnuti = document.getElementById("ukazat_shrnuti")
if (shrnuti["filename"] && ukazat_shrnuti) {
    let a = document.createElement("a")
    a.classList.add("link")
    a.href = "/file_api/vlastni_shrnuti/" + shrnuti["filename"]
    a.download = shrnuti["filename"]
    a.innerHTML = shrnuti["filename"]
    ukazat_shrnuti.appendChild(a)
}

// prace
let prace = JSON.parse(httpGet("/file_api/send_filenames_vlastni_prace"))
let ukazat_praci = document.getElementById("ukazat_praci")
if (prace) {
    for (let prace_file of prace) {
        let a = document.createElement("a")
        a.classList.add("link")
        a.href = "/file_api/vlastni_prace/" + prace_file
        a.download = prace_file
        a.innerHTML = prace_file
        ukazat_praci.appendChild(a)
        ukazat_praci.appendChild(document.createElement("br"))
    }
}

if (nahrane_shrnuti_input) {
    nahrane_shrnuti_input.addEventListener("change", function() {
        let spolecna_velikost = 0
        for (let file of this.files) {
            spolecna_velikost += file.size
        }
        if (spolecna_velikost > 5*1024*1024) {
            alert("Zajisti prosím, aby shrnutí práce nebylo větší než 5 MB. Pokud potřebuješ více místa, použij prosím jakékoli cloudové úložiště a sem nám pošli textový dokument, ve kterém bude sdílecí link.")
            this.value = "";
        }
    })
}

if (nahrana_prace_input) {
    nahrana_prace_input.addEventListener("change", function() {
        let spolecna_velikost = 0
        for (let file of this.files) {
            spolecna_velikost += file.size
        }
        if (spolecna_velikost > 20*1024*1024) {
            alert("Zajisti prosím, aby tvá  práce nebyla větší než 20 MB. Pokud potřebuješ více místa, použij prosím jakékoli cloudové úložiště a sem nám pošli textový dokument, ve kterém bude sdílecí link.")
            this.value = "";
        }
    })
}