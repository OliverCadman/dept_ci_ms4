$(document).on("submit", "div.modal-body form", function(e) {
    /*
    AJAX Request used for forms presented in modal windows.

    Required since forms in modals will not display errors upon
    page refresh. AJAX allows users to be made aware of errors 
    without closing the modal window.
    */
    e.preventDefault();
    const formElement = $(this);

    if (formElement.attr("id") === "edit_review_form") {
        return;
    }

    $.ajax({
        type: $(this).attr("method"),
        url: $(this).attr("action"),
        data: $(this).serialize(),
        success: function(data) {

            // If there are any validation errors...
            if (data.errors) {
                // Clears form of any errors present, to avoid duplicates.
                if ($(".form_error")) {
                    $(".form_error").remove();
              
                }
                let errorData = JSON.parse(data.errors);

                for (let name in errorData) {
                    if(errorData.hasOwnProperty(name)) {
                         let input = $("input[name='" + name + "']");
                         let textArea = $("textarea[name='" + name + "'");
                         if (input.attr("name") === "event_datetime") {
                           input
                             .next()
                             .parent()
                             .after(
                               `<p class="form_error secondary_font alert_style">${errorData[name][0].message}</p>`
                             );
                         } else {
                           input.after(
                             `<p class="form_error secondary_font alert_style">${errorData[name][0].message}</p>`
                           );
                         }
                         if (textArea) {
                           textArea.after(
                             `<p class="form_error secondary_font alert_style">${errorData[name][0].message}</p>`
                           );
                         }
                    }
                }
            } else {
                // If successful, display toast and refresh page after 2.5 seconds.
                let successMessage = data.success_msg;
                 Toastify({
                   text: successMessage,
                   duration: 2000,
                   close: true,
                   gravity: "top",
                   position: "right",
                   style: {
                     background: "#fefefe",
                     fontFamily: "'Josefin Sans', sans-serif",
                     color: "#17661a",
                   },
                 }).showToast();
                 setTimeout(() => {
                     location.reload();
                 }, 2000);
            }
        },
        error: function(data, options, thrownError) {
            formElement.parents(".modal-body").html(data);
        }
    });
});