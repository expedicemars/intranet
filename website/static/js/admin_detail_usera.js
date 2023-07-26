import httpGet from "./httpGet.js"
let id_usera = document.getElementById("id").value
let detail_usera = JSON.parse(httpGet("/admin_api/detail_usera/" + String(id_usera)))
let progressy = JSON.parse(httpGet("/admin_api/vsechny_progressy"))
let hodnoceni = JSON.parse(httpGet("/admin_api/hodnoceni/" + String(id_usera)))
let prace_filenames = JSON.parse(httpGet("/file_api/send_filenames_cizi_prace/" + String(id_usera)))
let ulozit_button = document.getElementById("ulozit_button")
let toggle_zmeny_button = document.getElementById("toggle_zmeny")
let charcount_span = document.getElementById("charcount")
let textarea = document.getElementById("admin_poznamka")
let meeting_link_input = document.getElementById("meeting_link")
let progress_select = document.getElementById("progress")
let odbornost_select = document.getElementById("odbornost_select")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))

ulozit_button.addEventListener("click", vyhodnotit)
toggle_zmeny_button.addEventListener("click", toggle_zmeny)
textarea.addEventListener("input", function() {
    charcount_span.innerHTML = String(textarea.value.length) + "/1000"
})

function toggle_zmeny() {
    let node = document.getElementById("uzamcene_zmeny")
    if (node.innerHTML == "Ne") {
        node.innerHTML = "Ano"
        toggle_zmeny_button.innerText = "Odemknout změny"
    } else {
        node.innerHTML = "Ne"
        toggle_zmeny_button.innerText = "Uzamknout změny"
    }
}

if (detail_usera.uzamcene_zmeny_bool) {
    toggle_zmeny_button.innerText = "Odemknout změny"
} else {
    toggle_zmeny_button.innerText = "Uzamknout změny"
}

function  vyhodnotit() {
    let result = {}
    result["odbornost"] = document.getElementById("odbornost_select").value
    result["progress"] = document.getElementById("progress").value
    if (document.getElementById("uzamcene_zmeny").innerHTML == "Ano") {
        result["uzamcene_zmeny"] = true
    } else {
        result["uzamcene_zmeny"] = false
    }
    result["admin_poznamka"] = textarea.value
    result["meeting_link"] = meeting_link_input.value
    document.getElementById("result").value = JSON.stringify(result)
    document.getElementById("form").submit()
}

// progressy
for (let prog of progressy) {
    let opt = document.createElement("option")
    opt.value = prog
    opt.id = prog
    opt.innerText = prog
    progress_select.appendChild(opt)
}


  // odbornost
dostupne_odbornosti.push(
    {
        "system_name": "zatím nevybraná",
        "prvnipjc": "zatím nevybraná"
    }
)
for (let odb of dostupne_odbornosti) {
    let opt = document.createElement("option")
    opt.value = odb.system_name
    opt.id = odb.system_name
    opt.innerText = odb.prvnipjc
    odbornost_select.appendChild(opt)
}

// spešl udaje, v else jsou ty normalni na display
for (let key in detail_usera) {
    let node = document.getElementById(key)
    if (node) {
        if (key == "id") {
            document.getElementById("id_display").innerHTML = detail_usera[key]
        } else if (key == "progress") {
            document.getElementById(detail_usera["progress"]).selected = "selected"
        } else if (key == "odbornost") {
            node.innerText = detail_usera[key]
            document.getElementById(detail_usera[key]).selected = "selected"
        } else if (key == "meeting_link") {
            meeting_link_input.value = detail_usera[key]
        } else {
            node.innerHTML = detail_usera[key]
        }
    }
}
charcount_span.innerHTML = String(textarea.value.length) + "/1000"

// shrnuti
let shrnuti = JSON.parse(httpGet("/file_api/send_filename_ciziho_shrnuti/" + String(id_usera)))
let ukazat_shrnuti = document.getElementById("ukazat_shrnuti")
if (shrnuti["filename"]) {
    let a = document.createElement("a")
    a.classList.add("link")
    a.href = "/file_api/cizi_shrnuti/" + String(id_usera) + "/" + shrnuti["filename"]
    a.download = shrnuti["filename"]
    a.innerHTML = shrnuti["filename"]
    ukazat_shrnuti.appendChild(a)
} else {
   ukazat_shrnuti.innerText = "Shrnutí práce ještě není odevzdané."
}

// shrnuti
let prace = JSON.parse(httpGet("/file_api/send_filenames_cizi_prace/" + String(id_usera)))
let ukazat_praci = document.getElementById("ukazat_praci")
if (prace) {
    for (let prace_file of prace) {
        let a = document.createElement("a")
        a.classList.add("link")
        a.href = "/file_api/cizi_prace/" + String(id_usera) + "/" + prace_file
        a.download = prace_file
        a.innerHTML = prace_file
        ukazat_praci.appendChild(a)
        ukazat_praci.appendChild(document.createElement("br"))
    }
} else {
   ukazat_praci.innerText = "Práce ještě není odevzdaná."
}

// motivacni formular
if (detail_usera["motivacni_formular"]) {
    document.getElementById("vyplneny_formular").hidden = false
    for (let odpoved of detail_usera["motivacni_formular"]) {
        document.getElementById(odpoved.id).innerHTML = odpoved.odpoved
    }
} else {
    document.getElementById("nevyplneny_formular").hidden = false
}


// hodnoceni
function create_div(content) {
    const div = document.createElement("div");
    div.classList.add("col-md", "rounded-2", "border-orange", "m-2", "p-2", "lighter");
    
    let table = document.createElement("table")
    table.classList.add("table", "table-hover")
    div.appendChild(table)
    let tbody = document.createElement("tbody")
    table.appendChild(tbody)

    function createTableRow(key, value) {
        let tr = document.createElement("tr");
        tbody.appendChild(tr);
        
        let td = document.createElement("td");
        tr.appendChild(td);

        let row = document.createElement("div")
        row.classList.add("row")
        td.appendChild(row)

        let col1 = document.createElement("div")
        col1.classList.add("col")
        let b = document.createElement("b")
        b.innerText = key
        
        row.appendChild(col1)
        col1.appendChild(b)
        
        let col2 = document.createElement("div")
        col2.classList.add("col")
        col2.innerText = value
        row.appendChild(col2)
        
        if (key == "K-faktor") {
            b.classList.add("rainbow")
            col2.classList.add("rainbow")
        }

    }
    createTableRow("Datum hodnocení", content["datum_zalozeni"]);
    createTableRow("Kdo hodnotil", content["admin_email"]);
    createTableRow("Věcnost", content["vecnost"]);
    createTableRow("Originalita", content["originalita"]);
    createTableRow("Komunikace", content["komunikace"]);
    createTableRow("Motivovanost", content["motivovanost"]);
    createTableRow("Sebevědomí", content["sebevedomi"]);
    createTableRow("Flexibilita", content["flexibilita"]);
    createTableRow("Sebehodnocení", content["sebehodnoceni"]);
    createTableRow("K-faktor", content["k_faktor"]);
    createTableRow("Dojem", content["dojem"]);

    let smazat_button = document.createElement("button")
    smazat_button.innerText = "Smmazat hodnocení"
    smazat_button.classList.add("btn", "btn-danger")
    smazat_button.type = "submit"
    smazat_button.value = content["id"]
    smazat_button.name = "smazat_hodnoceni"
    div.appendChild(smazat_button)

    return div;
  }

function createRowAndDivs(container, hodnoceni) {
    let row = document.createElement("div");
    row.classList.add("row");
  
    for (let i = 0; i < hodnoceni.length; i++) {
      const div = create_div(hodnoceni[i]);
      row.appendChild(div);
  
      // Check if two divs have been added to the row
      if ((i + 1) % 2 === 0 || i === hodnoceni.length - 1) {
        container.appendChild(row);
        row = document.createElement("div");
        row.classList.add("row");
      }
    }
  }
  
  const container = document.getElementById("hodnoceni_div");
  createRowAndDivs(container, hodnoceni);
