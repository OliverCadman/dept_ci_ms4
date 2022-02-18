$(document).ready(function() {
  let calendar;
  let dateArray = [];

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
        initCalendar();
      }
    });
  }

  function initCalendar() {
    const calendarElement = document.getElementById("calendar_wrapper");
    calendar = new FullCalendar.Calendar(calendarElement, {
      initialView: "dayGridMonth",
      selectable: true,
      height: 450,
      events: [],
      dateClick: function (info) {
        let events = createEvent(info.dateStr);
        dateArray.push(events);
      },
    });
    calendar.render();
  }

  function createEvent(startDate) {
    const event = {
      id: uuidv4(),
      date: startDate,
    };
    calendar.addEvent(event);
    dateArray.push(event);

    return dateArray;
  }

  function collectDateArray() {
    let dates = calendar.getEvents();
    console.log(dates);
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
    const username = $("#user_name_3").val();
    const csrfToken = $("input[name='csrfmiddlewaretoken']")[2].value;
    console.log(csrfToken);
    if (isSubmitting) {
      return;
    }
    isSubmitting = true;
    const url = `/profile/upload_unavailability/${username}`;
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