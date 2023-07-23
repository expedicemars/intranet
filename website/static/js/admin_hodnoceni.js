document.getElementById("form-check").addEventListener("click", function() {
    const names = [
        "vecnost",
        "originalita",
        "komunikace",
        "motivovanost",
        "sebevedomi",
        "flexibilita",
        "sebehodnoceni",
        "k_faktor"
      ]
    let all_checked = true
    for (let name of names) {
        let name_inputs = document.querySelectorAll("input[name='" + name + "']")
        let current_is_checked = false
        for (let input of name_inputs) {
            if (input.checked) {
                current_is_checked = true
                break
            }
        }

        if (!current_is_checked) {
            all_checked = false
            break
        }
    }
    if (all_checked) {
        document.getElementById("form").submit()
    } else {
        alert("Prosím, ohodnoť v každém kritériu.")
    }
})