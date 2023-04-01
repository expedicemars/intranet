import httpGet from "./httpGet.js"
let registrace = httpGet("/send_noauth/registrace")
let registrace_date_input = document.getElementById("registrace_date")
registrace_date_input.value=registrace
