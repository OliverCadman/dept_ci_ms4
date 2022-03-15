/* Used in 'Jobs' section of Dashboard:

---- TIER ONE ----

Details Modal:
  - Populates fields in modal displaying details of engagement.

Message Modal/Message Form:
  - Performs AJAX request to gather messages for given invitation, and populate modal if any messages are present.
  - Populates header of modal with message receiver's name.
  - Dynamically generates form action URL with relevant params required.

---- TIER TWO ---- 

Job Offer Modal:
  - Performs AJAX request to gather details of all members expressing interest in a posted job offer.
  - Populates the relative modal with details of all members expressing interest, with links to profile
    and button to confirm user.
*/

// TIER ONE 

const requestUserId = parseInt($("#request_user_id").val());

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
    const messageContainerId = "#message_display_container";
    const messageModalId = "#message_modal"
    let tierOneAjaxMessageGETUrl = `/bookings/get_invitation_messages/${invitationId}`;
            
    // Populate message modal with messages
    displayMessages(tierOneAjaxMessageGETUrl)
  });

  $(".tier_two_message_modal_btn").click(function() {
    const jobPostId = $(this).data("job-post-id");
    const tierTwoAjaxMessageGETUrl = `/bookings/get_invitation_messages/${jobPostId}`;
    displayMessages(tierTwoAjaxMessageGETUrl);

    $("#message_form").attr(
      "action",
      `/social/send_message/${$(this).data("invite-username")}/${jobPostId}`
    )
  })

  /* ---------------------------- */

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

  // - End of Tier One

  // TIER TWO

  // Job Post Modal

  $(".offers_received_modal_btn").click(function() {
    let jobId = $(this).data("job-id");

    $("#offers_received_modal_header").html(`
      ${$(this).data("job-offer-count")} members are interested.`)

    // AJAX Request to get details of members who have registered interest in a given job.
    $.ajax({
      url: `/jobs/get_interested_members/${jobId}`,
      type: "GET",
      success: function(res) {
        let interestedMembers = res.member_details

        // Populate relative modal with details of each member who registered interest.
        for (let member of interestedMembers) {
          
          let membersInstruments = member.instruments_played;
          membersInstruments = membersInstruments.join(", ");
        
          $("#interested_member_container").append(
            `
            <div class="col-12">
              <div class="job-card job_offer_modal">
                  <div class="invitation-card-header justify_between_row">
                    <div class="invitation-card-title">
                      <p class="primary_font med_small_text">${member.first_name} ${member.last_name}</p> 
                      <p class="primary_font light_weight"><span class="dashboard_card_icon"><i class="fa-solid fa-location-dot"></i></span>${member.city}, ${member.country}</p>
                    </div>
                    <img src="${member.profile_image}" alt="Member Avatar" class="modal_avatar" width="40" height="40">
                  </div>
                  <div class="invitation-card-body">
                      <p class="primary_font light_weight"><span class="dashboard_card_icon"><i class="fa-solid fa-guitar"></i></span>${membersInstruments}</p>
                  </div>
                  <div class="invitation-btn-wrapper">
                    <a href="/profile/${member.username}" class="btn primary_bg white_font secondary_font modal_btn mb-2 mt-3">Visit Profile</a>
                    <a href="/jobs/confirm_job_offer/${member.job_id}/${member.username}" class="btn custom_success secondary_font white_font modal_btn">Confirm ${member.first_name}</a>
                  </div>
              </div>
            </div>
            `
          );
        }
      }
    })
  })


  $("#offers_received_modal").on("hidden.bs.modal", function() {
    $("#interested_member_container").empty()
  })


function displayMessages(url) {
  let messageContainer = $("#message_display_container");

  $.ajax({
    type: "GET",
    url: url,
    success: function (res) {
      console.log(res.messages);
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
          messageElement.classList.add("message-content");

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
      displayAJAXErrorMessage(err.status);
    },
  });

  // Empty messages from message modal when modal is hidden
  $("#message_modal").on("hidden.bs.modal", function () {
    messageContainer.empty();
  });
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
