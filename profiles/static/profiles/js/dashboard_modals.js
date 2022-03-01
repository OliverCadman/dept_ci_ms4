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
    $("#message_modal_header").html(
      `${$(this).data("invite-fname")} ${$(this).data("invite-lname")}`
    );

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

        console.log(messages);
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
      error: function (err) {},
    });

    // Empty messages from message modal when modal is hidden
    $("#message_modal").on("hidden.bs.modal", function () {
      messageContainer.empty();
    });
  });

  // Format date to remove Python's TZ info in datetime object
  // and make it readable for the user.
  // https://stackoverflow.com/questions/25275696/javascript-format-date-time
  function formatDate(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    hours = hours % 24;
    hours = hours ? hours : 24;
    minutes = minutes < 10 ? "0" + minutes : minutes;

    let strTime = hours + ":" + minutes;
    return (
      date.getDate() +
      1 +
      "/" +
      (date.getMonth() + 1) +
      "/" +
      date.getFullYear() +
      " " +
      strTime
    );
  }

  // Calculate the difference between two dates (UTC Aware)
  // https://stackoverflow.com/questions/3224834/get-difference-between-2-dates-in-javascript
  const _MS_PER_DAY = 1000 * 60 * 60 * 24;

  function dateDiffInDays(a, b) {
    // Discard the time and time-zone information.
    const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
    const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

    return Math.floor((utc2 - utc1) / _MS_PER_DAY);
  }
})