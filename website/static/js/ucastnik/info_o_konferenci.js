import httpGet from "../httpGet.js"

let info_o_konferenci = httpGet("/user_api/info_o_konferenci")

document.getElementById("content").innerHTML = info_o_konferenci