/* Used in 'Jobs' section of Dashboard:

Details Modal:
- Populates fields in modal displaying details of engagement.

Messaage Form:
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
        $("#modal_additional").html("No Additional Information")
      }
    });

    $(".message_modal_btn").click(function() {
      $("#message_modal_header").html(`${$(this).data("invite-fname")} ${$(this).data("invite-lname")}`)
      $("#message_form").attr('action', `/social/send_message/${$(this).data("invite-username")}/${$(this).data("invitation-id")}`)
      
    })
})