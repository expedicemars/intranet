let button_ids = ["biolog", "fyzik", "konstrukter", "inzenyr", "popularizator"]
let form = document.getElementById("form")
let result = document.getElementById("result")

for (let id of button_ids) {
    document.getElementById(id).addEventListener("click", function() {
        if (confirm("Po vybrání odbornosti už tvoje volba nepůjde změnit. Jasný?")) {
            result.value = id
            form.submit()
        }
    })
}