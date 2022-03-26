$(document).ready(function() {
    /*
    Provides functionality to modal to edit a given review.

    Performs an AJAX request to view to return the current
    review content, and populate the modal form's textarea
    with the value.

    Upon submission of the form, check for any form errors
    (error will be thrown if content contains only numbers).
    If a successful submit, display a toast with a success
    message and refresh the page.
    */
    $(".edit_review_modal_trigger").click(function() {
        
        // AJAX GET request to retrieve current review.
        $.ajax({
            url: `/profile/get_review_to_edit/${$(this).data("review-id")}`,
            type: "GET",
            success: function(res) {
                // If Review does not exist, display toast with error message
                if (res.error) {
                    displayToast(res.error, "#9c1e1e")
                }
                const reviewContent = data.review;
                $("#review_edit").val(reviewContent);

            }
        })
        const editReviewURL = `/profile/edit_review/${$(this).data("review-id")}`

        // Set the form's action
        $("#edit_review_form").attr("action", editReviewURL);

        // Perform AJAX request on submit and check for errors or success.
        $("#edit_review_form").on("submit", function(e) {
            e.preventDefault();
              $.ajax({
                type: $(this).attr("method"),
                url: editReviewURL,
                data: $(this).serialize(),
                success: function (res) {
                  if (res.error) {
                    const error = res.error
                    let textArea = $("#review_edit");
                    textArea.after(
                    `<p class="form_error secondary_font alert_style">${error}</p>`
                    );
                  } else {
                      const successMsg = res.success_msg;
                      displayToast(successMsg, "#287e28")

                      setTimeout(() => {
                        location.reload();
                      }, 2000)
                  }
                },
                // If error, Display toast informing of error, with error status.
                error: function(err) {
                    displayAJAXErrorMessage(err.status);
                }
              });
        })
    })
})