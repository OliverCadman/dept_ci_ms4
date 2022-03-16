$(document).on("submit", "div.modal-body form", function(e) {
    /*
    AJAX Request used for forms presented in modal windows.

    Required since forms in modals will not display errors upon
    page refresh. AJAX allows users to be made aware of errors 
    without closing the modal window.
    */
    e.preventDefault();
    const formElement = $(this);

    $.ajax({
        type: $(this).attr("method"),
        url: $(this).attr("action"),
        data: $(this).serialize(),
        success: function(data) {

            // If there are any validation errors...
            if (data.errors) {
                // Clears form of any errors present, to avoid duplicates.
                if ($(".form_error")) {
                    $(".form_error").remove()
              
                }
                let errorData = JSON.parse(data.errors);

                for (let name in errorData) {
                     let input = $("input[name='" + name + "']");
                     if (input.attr("name") === "event_datetime") {
                         input.next().parent().after(
                             `<p class="form_error secondary_font alert_style">${errorData[name][0].message}</p>`
                         )
                     } else {
                        input.after(`<p class="form_error secondary_font alert_style">${errorData[name][0].message}</p>`);
                     }
                }
            } else {
                // If successful, display toast and refresh page after 2.5 seconds.
                let success_msg = "Invitation sent!"
                 Toastify({
                   text: success_msg,
                   duration: 2500,
                   close: true,
                   gravity: "top",
                   position: "right",
                   style: {
                     background: "#202020",
                     fontFamily: "'Josefin Sans', sans-serif",
                     color: "#fefefe",
                   },
                 }).showToast();
                 setTimeout(() => {
                     location.reload();
                 }, 2500);
            }
        },
        error: function(data, options, thrownError) {
            formElement.parents(".modal-body").html(data);
        }
    })

})