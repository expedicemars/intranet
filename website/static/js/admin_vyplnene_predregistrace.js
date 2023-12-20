import TableCreator from "./table_creator.js";
import httpGet from "./httpGet.js"

let mailing_list = JSON.parse(httpGet("/admin_api/mailing_list"))

let tc = new TableCreator(document.getElementById("parent_div"))

tc.make_header(["Datum", "E-mail", "Smazat"])
tc.make_tbody()

for (let mail of mailing_list) {
    let btn = document.createElement("button")
    btn.type = "submit"
    btn.classList.add("btn", "btn-danger")
    btn.innerText = "Smazat"
    btn.name = "smazat"
    btn.value = mail["email"]
    tc.make_row([mail["pretty"], mail["email"], btn], [0, 0, 0])
}