import TableCreator from "../table_creator.js";
import httpGet from "../httpGet.js"

let mailing_list = JSON.parse(httpGet("/admin_api/mailing_list"))

let tc = new TableCreator(document.getElementById("parent_div"))

tc.make_header(["#", "Datum", "E-mail", "Smazat"])
tc.make_tbody()

for (let i = 0; i<mailing_list.length; i++) {
    let mail = mailing_list[i]
    let btn = document.createElement("button")
    btn.type = "submit"
    btn.classList.add("btn", "btn-danger")
    btn.innerText = "Smazat"
    btn.name = "smazat"
    btn.value = mail["email"]
    tc.make_row([mailing_list.length - i, mail["pretty"], mail["email"], btn], [0, 0, 0, 0])
}

let mails = []
for (let m of mailing_list) {
    mails.push(m.email)
}


document.getElementById("zkopirovat_button").addEventListener("click", function() {
    let text = mails.join(", ")
    navigator.clipboard.writeText(text)
    this.innerText = "Hotovo"
    setTimeout(() => {
        this.innerText = "Znovu kopírovat"
    }, 1000);
})