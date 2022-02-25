$(document).ready(function() {
    $(".invitation_card_btn").click(function () {
      console.log("hello");
      $("#modal_event_name").html($(this).data("event-name"));
      $("#modal_invite_personage").html(
        `${$(this).data("invite-fname")}  ${$(this).data("invite-lname")}`
      );
      $("#modal_event_location").html(
        `${$(this).data("event-city")}, ${$(this).data("event-country")}`
      );
      $("#modal_event_datetime").html($(this).data("event-datetime"));
      $("#modal_event_additional").html($(this).data("additional-info"));
    });
})