$(document).ready(function() {



  let calendar;
  let dateArray = [];
  const userId = $("#user_id_3").val();
  const csrfToken = $("input[name='csrfmiddlewaretoken']")[2].value;

  /* Mutations observer listens for 'hidden' className change on calendar container.
           Calendar is only initialized when 'hidden' class is removed. */
  // https://nikitahl.com/listen-for-class-change-in-javascript
  const calendarContainer = document.getElementById("calendar_container");
  const options = {
    attributes: true,
  };

  const observer = new MutationObserver(callback);
  observer.observe(calendarContainer, options);
  function callback(mutationList, observer) {
    mutationList.forEach(function (mutation) {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "class"
      ) {
        const userId = $("#user_id_3").val();
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

  function initCalendar(existingUnavailableDates) {

    let eventArray = []
    let eventId = 1
    if (existingUnavailableDates) {
      for (date of existingUnavailableDates) {
        let eventObject = {
          id: eventId++,
          start: date,
          allDay: true,
          display: "background",
          backgroundColor: "#ee9ea2"
        }
        eventArray.push(eventObject)
      }
    }

    const calendarElement = document.getElementById("calendar_wrapper");
    calendar = new FullCalendar.Calendar(calendarElement, {
      initialView: "dayGridMonth",
      selectable: true,
      height: 450,
      headerToolbar: {
        left: "title",
        center: "",
        right: "prev,next"
      },
      events: eventArray,
      dateClick: function (info) {        
        const events = calendar.getEvents();
        let eventToRemove;
        for (let event of events) {  
          let eventDate = event.start.toISOString().split("T")[0];
          if (eventDate === info.dateStr) {
            eventToRemove = event;
          } 
        }
        if (eventToRemove) {
          console.log(eventToRemove.start.toISOString().split("T")[0]);
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
               console.log(res);
               eventToRemove.remove();
             },
           });
        } else {
          createEvent(info.dateStr)

        }
      },
    });
    calendar.render();
  }

  function createEvent(startDate) {
    const event = {
      id: uuidv4(),
      date: startDate,
      display: "background",
      backgroundColor: "#ee9ea2"
    };
    calendar.addEvent(event);
  
  }

  function collectDateArray() {
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

  const submitBtn = $("#submit_unavailability");
  let isSubmitting = false;

  submitBtn.on("click", function () {
    let dateArray = collectDateArray();
    console.log(csrfToken);
    if (isSubmitting) {
      return;
    }
    isSubmitting = true;
    const url = `/profile/upload_unavailability/${userId}`;
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

        $("#third_breadcrumb_sm").addClass("fill-breadcrumb-sm");
        $("#third_breadcrumb_icon").addClass("fill-breadcrumb-icon-sm");
        $("#third_breadcrumb").addClass("fill-breadcrumb");
        $("#third_breadcrumb_text").addClass("dark-text");

        Toastify({
          text: res.success_msg,
          duration: 10000,
          close: true,
          gravity: "top",
          position: "right",
          style: {
            background: "#202020",
            fontFamily: "'Josefin Sans', sans-serif",
            color: "#fefefe",
          },
        }).showToast();
        setTimeout(() => {
          window.location.href = res.url;
        }, 2500);
      },
    });
    return false;
  });

  function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
      (
        c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
      ).toString(16)
    );
  }
})