$(document).ready(function() {
    const addMoreBtn = document.getElementById("add_more_btn")

    addMoreBtn.addEventListener("click", addMoreForms)

    function addMoreForms(e) {
        e.preventDefault();
    }
})