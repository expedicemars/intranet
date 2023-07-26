import httpGet from "./httpGet.js"
let odpovedi_motivaku = JSON.parse(httpGet("/user_api/odpovedi_motivaku"))

 for (let o of odpovedi_motivaku) {
    document.getElementById(o.id).innerText = o.odpoved
 }

let shrnuti = JSON.parse(httpGet("/file_api/send_filename_vlastniho_shrnuti"))
let ukazat_shrnuti = document.getElementById("ukazat_shrnuti")
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