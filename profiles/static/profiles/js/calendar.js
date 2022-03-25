$(document).ready(function() {

  /* Initialize Global Variables */
  let calendar;

  // UserId and csrf token to use in POST request
  const userId = $("#user_id_3").val();
  const csrfToken = $("input[name='csrfmiddlewaretoken']")[2].value;

  /* Mutations observer listens for 'hidden' className change on calendar container.
           Calendar is only initialized when 'hidden' class is removed. */
  // https://nikitahl.com/listen-for-class-change-in-javascript
  const calendarContainer = document.getElementById("calendar_container");
  const options = {
    attributes: true,
  };


  // Check for "hidden" className change on calendar container.

  /* When fired, an AJAX call is made to the backend to get user's 
     unavailable dates. */
  const observer = new MutationObserver(callback);
  observer.observe(calendarContainer, options);
  function callback(mutationList, observer) {
    mutationList.forEach(function (mutation) {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "class"
      ) {
        $.ajax({
          url: `/profile/get_users_unavailable_dates/${userId}`,
          type: "get",
          dataType: "json",
          success: function (res) {
            initCalendar(res.unavailable_dates);
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
      }
    });
  }

// ------------------------------------------------------

  function initCalendar(existingUnavailableDates) {
    /* Initialize the FullCalendar, and populate with
    any existing dates returned from the backend, if any.
    */

    let eventArray = [];
    let eventId = 1;
    if (existingUnavailableDates) {
      for (date of existingUnavailableDates) {
        let eventObject = {
          id: eventId++,
          start: date,
          allDay: true,
          display: "background",
          backgroundColor: "#ee9ea2",
        };
        eventArray.push(eventObject);
      }
    }

    // Create the Calendar with initialView, toolbar styling, and events
    const calendarElement = document.getElementById("calendar_wrapper");
    calendar = new FullCalendar.Calendar(calendarElement, {
      initialView: "dayGridMonth",
      height: 450,
      headerToolbar: {
        left: "title",
        center: "",
        right: "prev,next",
      },
      events: eventArray,
    });
    calendar.render();

    // Event handler for dateClick, call function logDate()
    calendar.on("dateClick", logDate, { passive: true });

    function logDate(info) {
      /* 
        Event handler to log clicked dates.

        If the date-string of the clicked date
        matches a date already in the collection
        of FullCalendar's events (populated with
        AJAX 'get_users_unavailable_dates'), then 
        make an AJAX POST request to remove the date
        from the calendar.

        Otherwise, create a calendar event from the clicked
        date.
        */
      const events = calendar.getEvents();
      let eventToRemove;
      for (let event of events) {
        let eventDate = event.start.toISOString().split("T")[0];
        if (eventDate === info.dateStr) {
          eventToRemove = event;
        }
      }

      // If there is an event to remove, make post request to remove.
      if (eventToRemove) {
        $.post({
          url: `/profile/upload_unavailability/${userId}`,
          data: {
            event_to_remove: eventToRemove.start.toISOString().split("T")[0],
            request: 2,
          },
          headers: {
            "X-CSRFToken": csrfToken,
          },
          success: function (res) {
            eventToRemove.remove();
          },
        });
      } else {
        // Otherwise, create an event
        createEvent(info.dateStr);
      }
    }
  }

  function createEvent(startDate) {
    /* 
      Creates a FullCalendar event, with
      id, startDate and styling. 
      */
    const event = {
      id: uuidv4(),
      date: startDate,
      display: "background",
      backgroundColor: "#ee9ea2",
    };
    calendar.addEvent(event);
  }

  function uuidv4() {
    /* Creates a unique identifier for a created FullCalendar Event  */
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
      (
        c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
      ).toString(16)
    );
  }

   function collectDateArray() {
        /*
          Collects dates added to FullCalendar's
          collection of added events, and prepares
          them into the correct format, to be posted
          to the backend.
        */
        let dates = calendar.getEvents();
        let ISOStringFormattedDateArray = [];

        for (let i = 0; i < dates.length; i++) {
            let rawDateString = dates[i]._instance.range.start
            .toISOString()
            .split("T")[0];
            ISOStringFormattedDateArray.push(rawDateString);
         }

        return ISOStringFormattedDateArray;
   }

  // ---------- Submit Unavailable Dates ---------- //
  const submitBtn = $("#submit_unavailability");
  let isSubmitting = false;

  submitBtn.on("click", function () {
      let dateArray = collectDateArray();

      // Removes any duplicate dates from dateArray
      dateArray = [...new Set(dateArray)];

      // Avoids duplicate post requests
      if (isSubmitting) {
          return;
        }
      isSubmitting = true;
      const url = `/profile/upload_unavailability/${userId}`;

      // Post to /profile/upload_unavailability URL
      $.post({
          url: url,
          headers: {
              "X-CSRFToken": csrfToken,
          },
          data: {
            date_array: dateArray,
          },
          success: function (res) {
              isSubmitting = false;

              /* Fill third breadcrumb upon successful submission
              and display toast. Then redirect.
              */
              $("#third_breadcrumb_sm").addClass("fill-breadcrumb-sm");
              $("#third_breadcrumb_icon").addClass("fill-breadcrumb-icon-sm");
              $("#third_breadcrumb").addClass("fill-breadcrumb");
              $("#third_breadcrumb_text").addClass("dark-text");

              const successMsg = "You updated your calendar.";
              displayToast(successMsg, "#287e28");

              setTimeout(() => {
                  window.location.href = res.url;
              }, 2500);
          },
          error: function (err) {
              console.log(err);
          },
       });
       return false;
  });
})