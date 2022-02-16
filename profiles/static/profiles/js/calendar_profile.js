/* AJAX call to get unavailable dates inputted by user in the 'Edit Profile' page.
  If a value is returned, it is passed into a function which initializes a FullCalendar 
  instance, with an array of event objects included in the initialization arguments.
*/


$(document).ready(function() {
    // Username grabbed from invisible input element's value
    console.log("hello")
    const username = $("#username").val()
    $.ajax({
        url: `/profile/get_users_unavailable_dates/${username}`,
        type: "get",
        dataType: "json",
        success: function(res){ 
            generateUnavailabilityCalendar(res.unavailable_dates)
            },
        error: function(err) {
            const message = "Sorry, there was an internal server error. Please try again"
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
        }
    })

     function generateUnavailabilityCalendar(ajaxResponse) {
       let dateList = ajaxResponse;
       let eventArray = [];

       for (date of dateList) {
         let eventObject = {
           start: date,
           allDay: true,
         };

         eventArray.push(eventObject);
       }

       const calendarElement = document.getElementById("calendar_wrapper");
       calendar = new FullCalendar.Calendar(calendarElement, {
         initialView: "dayGridMonth",
         events: eventArray,
       });

       calendar.render();
     }
    
})

