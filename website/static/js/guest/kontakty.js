import httpGet from "../httpGet.js"
document.getElementById("velitel_internetovych_kol_mail").innerHTML = httpGet("/noauth_api/velitel_internetovych_kol_mail")
