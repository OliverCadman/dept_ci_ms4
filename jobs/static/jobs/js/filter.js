$(document).ready(function() {
    /*
    JavaScript code to allow user to execute search
    immediately upon selecting a search criteria in the
    form select dropdown list.
    */

    // Grab select element and attach 'onchange' event listener.
    const selectEl = $("#instrument_filter")
    selectEl.on("change", function() {
        let parentFormId = "#instrument_filter_form"
        FilterOnSelectChange(parentFormId)
    })


    function FilterOnSelectChange(formId) {
        /* Submits the form immediately upon change of select value
        
        Params: 

            formId - If of the parent form to submit.
        */
        let form = $(formId)
        if (typeof(form) != undefined || typeof(form) != null) {
            form.submit();
        }
    }
})