import httpGet from "./httpGet.js"

let moje_info = JSON.parse(httpGet("/user_api/moje_info"))

for (let zaznam of moje_info) {
    if (zaznam["nadpis"] == "Obecné") {
        document.getElementById("obecne_content").innerHTML = zaznam["content"]
    } else {
        document.getElementById("to_druhe").innerText = zaznam["nadpis"]
        document.getElementById("to_druhe_content").innerHTML = zaznam["content"]
    }
}