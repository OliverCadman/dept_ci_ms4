/* 
    Enables switching of form pages in Edit Profile form.
    Page switching is mimiced through the hiding of the AudioForm
    element and the showing of the FullCalendar element.
*/

// let username = $("#request_user").text();

// // Trims the quotes off the "request_user" value
// username = username.replace(/\"/g, "");

$("#skip_audio_form").click(
  {
    param1: "#add_audio_container",
    param2: "hidden",
    param3: "#calendar_container",
    param4: $(".edit_profile_header"),
    param5: $(".profile-prompt-lead"),
    param6: availabilityHeader,
    param7: avaliabilityLead,
  },
  switchStep
);

$("#skip_calendar_form").click(
  {
    param1: "#calendar_container",
  },
  switchStep
);

// Skip from Audio Dropzone to Unavailability Calendar,
// or Unavailability Calendar back to home page.
function switchStep(event) {
  const el1 = $(event.data.param1);
  const el2 = $(event.data.param3);
  console.log(el1.attr("id"));

  if (el1.attr("id") !== "calendar_container") {
    el1.addClass(event.data.param2);
    el2.removeClass(event.data.param2);

    let availabilityHeader = event.data.param4;
    let availabilityLead = event.data.param5;
    let headerContent = event.data.param6;
    let leadContent = event.data.param7;

    changeHeader(
      availabilityHeader,
      availabilityLead,
      headerContent,
      leadContent
    );
  } else {
    window.location.href = `/profile/${username}`;
  }
}

function changeHeader(headerEl, leadEl, header, lead) {
  const el1 = headerEl;
  const el2 = leadEl;

  const headerContent = header;
  const leadContent = lead;

  el1.html(headerContent);
  el2.html(leadContent);
}
