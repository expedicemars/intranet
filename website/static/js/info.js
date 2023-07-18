import httpGet from "./httpGet.js"
let odpovedi_motivaku = JSON.parse(httpGet("/user_api/odpovedi_motivaku"))

 for (let o of odpovedi_motivaku) {
    document.getElementById(o.id).innerText = o.odpoved
 }