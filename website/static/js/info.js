import httpGet from "./httpGet.js"
let odpovedi_motivaku = JSON.parse(httpGet("/user_api/odpovedi_motivaku"))
let dalsi_kroky_div = document.getElementById("dalsi_kroky")
let dalsi_kroky_info = httpGet("/user_api/dalsi_kroky")
let shrnuti = JSON.parse(httpGet("/file_api/send_filename_vlastniho_shrnuti"))
let ukazat_shrnuti = document.getElementById("ukazat_shrnuti")
let prace = JSON.parse(httpGet("/file_api/send_filenames_vlastni_prace"))
let ukazat_praci = document.getElementById("ukazat_praci")

if (document.getElementById("odevzdany_formular")) {
   for (let o of odpovedi_motivaku) {   
      document.getElementById(o.id).innerText = o.odpoved
   }
}

if (shrnuti["filename"]) {
    let a = document.createElement("a")
    a.classList.add("link")
    a.href = "/file_api/vlastni_shrnuti/" + shrnuti["filename"]
    a.download = shrnuti["filename"]
    a.innerHTML = shrnuti["filename"]
    ukazat_shrnuti.appendChild(a)
} else {
   ukazat_shrnuti.innerText = "Shrnutí práce ještě není odevzdané."
}

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
} else {
   ukazat_praci.innerText = "Práce ještě není odevzdaná."
}

dalsi_kroky_div.innerHTML = dalsi_kroky_info