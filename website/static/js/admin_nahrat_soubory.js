import httpGet from "./httpGet.js"
let soubory_existuji = JSON.parse(httpGet("/admin_api/soubory_existuji"))
let prohlaseni_link_div = document.getElementById("prohlaseni_link")
let dostupne_odbornosti = JSON.parse(httpGet("/noauth_api/dostupne_odbornosti"))
let content_form = document.getElementById("content")

if (soubory_existuji["prohlaseni_rodicu"]) {
    let a = document.createElement("a")
    a.innerHTML = "Stáhnout současnou verzi"
    a.href = "/file_api/prohlaseni_rodicu"
    a.download = "prohlaseni_rodicu.docx"
    prohlaseni_link_div.appendChild(a)
    a.classList.add("link")
} else {
    prohlaseni_link_div.innerHTML = "Žádné prohlášení tu ještě nahrané není."
}

for (let odb of dostupne_odbornosti) {
    content_form.appendChild(document.createElement("hr"))
    // Create the main container div
    const containerDiv = document.createElement('div');
    containerDiv.className = 'container';

    // Create the heading
    const heading = document.createElement('h3');
    heading.textContent = 'Šablona shrnutí práce pro ' + odb.ctvrtypmc;
    containerDiv.appendChild(heading);

    // Create the row div
    const rowDiv = document.createElement('div');
    rowDiv.className = 'row';

    // Create the first column div for the text
    const colTextDiv = document.createElement('div');
    colTextDiv.className = 'col-auto';
    colTextDiv.textContent = 'Nahrát novou verzi:';
    rowDiv.appendChild(colTextDiv);

    // Create the second column div for the file input
    const colInputDiv = document.createElement('div');
    colInputDiv.className = 'col';

    const inputFile = document.createElement('input');
    inputFile.type = 'file';
    inputFile.className = 'form-control';
    inputFile.name = odb.system_name + "_file";
    inputFile.accept = '.docx';

    colInputDiv.appendChild(inputFile);
    rowDiv.appendChild(colInputDiv);

    // Create the third column div for the button
    const colButtonDiv = document.createElement('div');
    colButtonDiv.className = 'col-auto';

    const uploadButton = document.createElement('button');
    uploadButton.className = 'btn em-button';
    uploadButton.type = 'submit';
    uploadButton.textContent = 'Nahrát';
    uploadButton.name = odb.system_name
    uploadButton.value = "whatever"

    colButtonDiv.appendChild(uploadButton);
    rowDiv.appendChild(colButtonDiv);

    // Append the row div to the container div
    containerDiv.appendChild(rowDiv);

    // Create the div for "link"
    const link_div = document.createElement('div');
    link_div.id = odb.system_name + '_link';

    // Append the "prohlaseni_link" div to the container div
    containerDiv.appendChild(link_div);

    // Append the container div to the body or any other parent element
    content_form.appendChild(containerDiv);


    if (soubory_existuji[odb.system_name]) {
        let a = document.createElement("a")
        a.innerHTML = "Stáhnout současnou verzi"
        a.href = "/file_api/stahnout_sablonu/" + odb.system_name
        a.download = odb.system_name + "_sablona.docx"
        link_div.appendChild(a)
        a.classList.add("link")
    } else {
        link_div.innerHTML = "Žádné prohlášení tu ještě nahrané není."
    }

}