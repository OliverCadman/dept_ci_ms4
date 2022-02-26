$(document).ready(function() {
    $(".view_detail_btn").click(function (e) {
      e.stopPropagation();
      console.log("hello");
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
    })
})