/* AJAX call to get unavailable dates inputted by user in the 'Edit Profile' page.
  If a value is returned, it is passed into a function which initializes a FullCalendar 
  instance, with an array of event objects included in the initialization arguments.
*/

$(document).ready(function () {
  // UserId grabbed from invisible input element's value
  const userId = $("#user_id").val();
  $.ajax({
    url: `/profile/get_users_unavailable_dates/${userId}`,
    type: "get",
    dataType: "json",
    success: function (res) {
      generateUnavailabilityCalendar(res.unavailable_dates);
    },
    error: function (err) {
      const message =
        "Sorry, there was an internal server error. Please try again";
      Toastify({
        text: message,
        duration: 10000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
          background: "#ff7086",
          fontFamily: "'Josefin Sans', sans-serif",
          color: "#202020",
        },
      }).showToast();
    },
  });

  function generateUnavailabilityCalendar(ajaxResponse) {
    /*
          Create a FullCalendar instance, populated with
          dates returned from AJAX call (/profile/get_users_unavailable_dates)
         */
    let dateList = ajaxResponse;
    let eventArray = [];

    // Create a FullCalendar event for each date in the response.
    for (let date of dateList) {
      let eventObject = {
        start: date,
        allDay: true,
        display: "background",
        backgroundColor: "#ee9ea2",
      };

      eventArray.push(eventObject);
    }

    // Initialize and render the calender, with events added
    const calendarElement = document.getElementById("calendar_wrapper");
    const calendar = new FullCalendar.Calendar(calendarElement, {
      initialView: "dayGridMonth",
      height: 300,
      headerToolbar: {
        center: "",
        right: "prev next",
      },
      events: eventArray,
      dayHeaders: false,
    });

    calendar.render();
  }
});
