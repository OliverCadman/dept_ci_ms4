$(document).ready(function() {
    const addMoreBtn = document.getElementById("add_more_btn")

    addMoreBtn.addEventListener("click", addMoreForms)

    function addMoreForms(e) {
        e.preventDefault();

        const formCopyTarget = document.getElementById("equipment_form_list");
        const emptyFormElement = document
          .getElementById("empty_form")
          .cloneNode(true);

        emptyFormElement.setAttribute("class", "equipment_form");

        formCopyTarget.append(emptyFormElement);
    }
})