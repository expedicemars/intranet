import httpGet from "./httpGet.js"
let id_usera = document.getElementById("id").value
let detail_usera = JSON.parse(httpGet("/admin_api/detail_usera/" + String(id_usera)))
let progressy = JSON.parse(httpGet("/admin_api/vsechny_progressy"))
let prace_filenames = JSON.parse(httpGet("/file_api/send_filenames_cizi_prace/" + String(id_usera)))
let ulozit_button = document.getElementById("ulozit_button")
let toggle_zmeny_button = document.getElementById("toggle_zmeny")
let toggle_souhlas_button = document.getElementById("toggle_souhlas")
let charcount_span = document.getElementById("charcount")
let textarea = document.getElementById("admin_poznamka")
let meeting_link_input = document.getElementById("meeting_link")
let progress_select = document.getElementById("progress")


ulozit_button.addEventListener("click", vyhodnotit)
toggle_zmeny_button.addEventListener("click", toggle_zmeny)
toggle_souhlas_button.addEventListener("click", toggle_souhlas)
textarea.addEventListener("input", function() {
    charcount_span.innerHTML = String(textarea.value.length) + "/1000"
})

function toggle_zmeny() {
    let node = document.getElementById("uzamcene_zmeny")
    if (node.innerHTML == "false") {
        node.innerHTML = "true"
    } else {
        node.innerHTML = "false"
    }
}

function toggle_souhlas() {
    let node = document.getElementById("souhlas_rodicu")
    if (node.innerHTML == "false") {
        node.innerHTML = "true"
    } else {
        node.innerHTML = "false"
    }
}


function  vyhodnotit() {
    let result = {}
    result["progress"] = document.getElementById("progress").value
    result["uzamcene_zmeny"] = document.getElementById("uzamcene_zmeny").innerHTML
    result["souhlas_rodicu"] = document.getElementById("souhlas_rodicu").innerHTML
    result["admin_poznamka"] = textarea.value
    result["meeting_link"] = meeting_link_input.value
    document.getElementById("result").value = JSON.stringify(result)
    document.getElementById("form").submit()
}

for (let prog of progressy) {
    let opt = document.createElement("option")
    opt.value = prog
    opt.id = prog
    opt.innerText = prog
    progress_select.appendChild(opt)
}

for (let key in detail_usera) {
    let node = document.getElementById(key)
    if (node) {
        if (key == "id") {
            document.getElementById("id_display").innerHTML = detail_usera[key]
        } else if (key == "progress") {
            document.getElementById(detail_usera["progress"]).selected = "selected"         
        } else if (key == "meeting_link") {
            meeting_link_input.value = detail_usera[key]
        } else {
            node.innerHTML = detail_usera[key]
        }
    }
}
charcount_span.innerHTML = String(textarea.value.length) + "/1000"


if (prace_filenames) {
    document.getElementById("prace_disclaimer").hidden = true
    let prace_div = document.getElementById("prace_div")
    for (let filename of prace_filenames) {
        let a = document.createElement("a")
        a.innerHTML = filename
        a.download = filename
        a.href = "/file_api/cizi_prace/" + String(id_usera) + "/" + filename
        prace_div.appendChild(a)
        prace_div.appendChild(document.createElement("br"))
    }
} else {
    document.getElementById("prace_disclaimer").hidden = false
}
