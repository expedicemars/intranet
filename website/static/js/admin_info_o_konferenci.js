import httpGet from "./httpGet.js"

let info_o_konferenci = httpGet("/admin_api/info_o_konferenci")
let textarea = document.getElementById("content")
let preview_div = document.getElementById("preview_div")
let preview_button = document.getElementById("preview")

textarea.value = info_o_konferenci
preview_div.innerHTML = info_o_konferenci

preview_button.addEventListener("click", function() {
    preview_div.innerHTML = textarea.value
})
