/* Used in 'Jobs' section of Dashboard:

Details Modal:
- Populates fields in modal displaying details of engagement.

Message Modal/Message Form:
- Performs AJAX request to gather messages for given invitation, and populate modal if any messages are present.
- Populates header of modal with message receiver's name.
- Dynamically generates form action URL with relevant params required.

*/

$(document).ready(function() {
  $(".view_detail_btn").click(function (e) {
    $("#modal_event_name").html($(this).data("event-name"));
    $("#modal_invite_personage").html(
      `${$(this).data("invite-fname")}  ${$(this).data("invite-lname")}`
    );
    $("#modal_event_location").html(
      `${$(this).data("event-city")}, ${$(this).data("event-country")}`
    );
    $("#modal_event_datetime").html($(this).data("event-datetime"));

    if ($(this).data("additional-info") !== undefined) {
      $("#modal_additional").html($(this).data("additional-info"));
    } else {
      $("#modal_additional").html("No Additional Information");
    }
  });

  //
  $(".message_modal_btn").click(function () {
    console.log($(this).data("invite-fname"));
    console.log($(this).data("modal-profile-img"));
    if ($(this).data("modal-profile-img") != "") {
      $("#message_modal_header").html(
        `<img src=${$(this).data("modal-profile-img")} alt="${$(this).data("invite-fname")}" width="100" height="100" class="modal_profile_img">
        ${$(this).data("invite-fname")} ${$(this).data("invite-lname")}`
      );
    } else {
      $("#message_modal_header").html(
        `<img src="/media/dept-logo.webp" alt="${$(this).data(
          "invite-fname"
        )}" width="100" height="100" class="modal_profile_img">
        ${$(this).data("invite-fname")} ${$(this).data("invite-lname")}`
      );
    }

    // Form action with dynamic URL params passed from data attributes of 'message_modal_btn'
    $("#message_form").attr(
      "action",
      `/social/send_message/${$(this).data("invite-username")}/${$(this).data(
        "invitation-id"
      )}`
    );

    const invitationId = $(this).data("invitation-id");
    const requestUserId = parseInt($("#request_user_id").val());

    const messageContainer = $("#message_display_container");

    // AJAX GET request to populate modal with sent messages
    $.ajax({
      type: "GET",
      url: `/bookings/get_invitation_messages/${invitationId}`,
      success: function (res) {
        const messages = res.messages;

        if (messages.length > 0) {
          for (let messageObject of messages) {
            let messageDateTime = new Date(messageObject.date_of_message);

            let formattedDate = formatDate(messageDateTime);

            // Compare today's date with datetime object of message
            // Render time of message without date if message was sent today.
            const now = new Date();

            dateDiff = dateDiffInDays(messageDateTime, now);
            let timeNoDate;
            if (dateDiff < 2) {
              timeNoDate = formattedDate.split(" ")[1];
            }

            // Create message elemets and populate with data as content
            let messageWrapper = document.createElement("div");
            let dateTimeSpan = document.createElement("span");
            dateTimeSpan.classList.add("message-datetime");
            dateTimeSpan.innerText = dateDiff < 1 ? timeNoDate : formattedDate;

            let messageContent = messageObject.message;
            let messageElement = document.createElement("p");
            messageElement.classList.add("message-content")

            messageWrapper.classList.add("message");
            let messageSender = messageObject.message_sender;

            // Places sent message on left of containing div, and received message on right.
            if (messageSender === requestUserId) {
              messageWrapper.classList.add("sender");
            } else {
              messageWrapper.classList.add("receiver");
            }

            messageWrapper.append(dateTimeSpan);
            messageWrapper.append(messageElement);
            messageElement.innerText = messageContent;
            messageContainer.append(messageWrapper);

            /* Remove 'centered' class in the case that a user 
                  visits a populated message modal after visiting an 
                  unpopulated message modal */
            if (messageContainer.hasClass("centered")) {
              messageContainer.removeAttr("class");
            }
          }
        } else {
          messageContainer.addClass("centered");
          const noResultsEl = document.createElement("p");
          const noResultsMsg = "Start a Conversation";
          noResultsEl.innerText = noResultsMsg;
          messageContainer.append(noResultsEl);
        }
      },
      error: function (err) {
        displayAJAXErrorMessage(err.status)
      },
    });


    // Empty messages from message modal when modal is hidden
    $("#message_modal").on("hidden.bs.modal", function () {
      messageContainer.empty();
    });
  });

  /* Open Message Modal if user visits from Booking Detail page
  by clicking 'Message <user>' button. 
  
  Grabs the ID of the booking and performs AJAX request to
  get invitation ID of that booking.

  Invitation ID is compared against data-invitation-id attributes
  of .message_modal_btn. If one matches, that specific modal is triggered.
  */
  const referrer = document.referrer;
  const referrerPath = referrer.split("/")
  const referrerPageName = referrerPath[3]
  const bookingId = referrerPath[5]

  // AJAX Request
  if (referrerPageName === "bookings") {
      $.ajax({
        url: `/bookings/get_invitation_id/${bookingId}`,
        type: "get",
        success: function(res) {
          // Compare data-invitation-id attribute with returned Invitation ID
          const invitationId = res.invitation_id
          $(".message_modal_btn").each(function(){
              if ($(this).data("invitation-id") === invitationId) {
                $(this).trigger("click")
              }
          })
        },
        error: function(err) {
          displayAJAXErrorMessage(err.status)
        }
      })

  }
  
  // Displays a Toast with error message in case of AJAX errors
  function displayAJAXErrorMessage(status) {
      if (status === 0) {
        errorMsg = "Cannot connect, please make sure you are connected";
      } else if (status === 404) {
        errorMsg = `${status} error. We apologize; the resource was not found.`;
      } else if (status === 500) {
        errorMsg = `${status} error. We apologize. There is an internal server error.`;
      } else {
        errorMsg =
          "We apologize, there has been an error. We are working hard to rectify this.";
      }

      Toastify({
        text: errorMsg,
        duration: 10000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
          background: "#ff7086",
          fontFamily: "'Oxygen', sans-serif",
          color: "#202020",
        },
      }).showToast();
  }
})