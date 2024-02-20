import httpGet from "../httpGet.js"
let odpovedi_motivaku = JSON.parse(httpGet("/user_api/odpovedi_motivaku"))

for (let i=1;i<=14;i++) {
    let node = document.getElementById(String(i))
    if (node) {
        for (let entry of odpovedi_motivaku) {
            if (entry.id == i) {
                node.value = entry.odpoved
            }
        }
    }
}