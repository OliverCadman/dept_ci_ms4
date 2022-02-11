$(document).ready(function() {
   $("#audio_submit_btn").on("click", function() {
       setTimeout(() => {
           const dateArray = []
           let clickCount = 0;
           const calendarElement = document.getElementById("calendar_wrapper")
           const calendar = new FullCalendar.Calendar(calendarElement, {
               initialView: "dayGridMonth",
               dateClick: function(e) {
                   clickCount++
                   if (!e.dayEl.classList.contains("selected")) {
                       e.dayEl.classList.add("selected")
                       console.log(e.dayEl)
                       dateArray.push(e.dateStr);
                         dateArray.sort()
       
                   } else  {
                       e.dayEl.classList.remove("selected")
                       let dateToRemove = e.dateStr
                       let dateIndex = dateArray.indexOf(dateToRemove)
                       dateArray.splice(dateIndex, 1)
                       dateArray.sort()     
                   }
       
                   collectDateArrayAndSubmit(dateArray)
               }
       
           });
           calendar.render();
       },1700)
   }) 

    let isSubmitting = false;

    function collectDateArrayAndSubmit(array){
        const csrfToken = $("input[name='csrfmiddlewaretoken']")[2].value
        const dateArray = array
        const formData = new FormData();
        console.log(dateArray)
        const username = $("#user_name_3").val()
        
        const submitBtn = $("#submit_unavailability");
        submitBtn.on("click", function() {
            if (isSubmitting) {
                return; 
            }
            isSubmitting = true;
            console.log('click')
            const url = `/profile/upload_unavailability/${username}`;
            $.post({
            url: url,
            headers: {
                "X-CSRFToken": csrfToken,
            },
            data: {
                "date_array": dateArray
            },
            success: function (res) {
                isSubmitting = false;
                
                $("#third_breadcrumb_sm").addClass("fill-breadcrumb-sm")
                $("#third_breadcrumb_icon").addClass("fill-breadcrumb-icon-sm")
                $("#third_breadcrumb").addClass("fill-breadcrumb")
                $("#third_breadcrumb_text").addClass("dark-text")

            },
            }); 
            return false;
        })
    }
})