/* Dropzone JS

Creates a new Dropzone instance, to allow for drag and drop of audio files
on the website's 'Edit Profile' page.

https://docs.dropzone.dev/
*/
let username = $("#request_user").text()
username = username.replace(/\"/g, "");
console.log(username)


// Dropzone.autoDiscover = false;
Dropzone.options.audioDropzone = {
  method: "post",
  autoProcessQueue: false,
  paramName: "audio",
  maxFilesize: 30,
  clickable: true,
  uploadMultiple: true,
  // Remove tracks if necessary
  addRemoveLinks: true,
  acceptedFiles: ".mp3,.mp4,.m4a,.wav,.aac,.flac",
  maxFiles: 5,
  headers: {
    "X-CSRFToken": $("input[name=csrfmiddlewaretoken]")[1].value,
  },
  previewTemplate: `
        <div class="dz-preview dz-file-preview">
            <div class="dz-image">
                <img data-dz-thumbnail />
            </div>
            <div class="dz-details">
                <div class="dz-filename"><span data-dz-name></span></div>
            <div class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
                <div class="progress-bar progress-bar-success" style="width:0%;" data-dz-uploadprogress></div>
            </div>
            <div class="dz-size" data-dz-size></div>
        </div>
        <div class="dz-error-mark">✘</div>
        <div class="dz-error-message"><span data-dz-errormessage></span></div>
        </div>
    `,
  removedfile: function(file) {
    console.log(file)
     let filename = file.name;

     $.ajax({
       type: "post",
       url: `/profile/upload_audio/${username}`,
       data: {
         filename: filename,
         request: 2,
       },
       headers: {
         "X-CSRFToken": $("input[name=csrfmiddlewaretoken]")[1].value,
       },
       success: function () {
         file.previewElement.remove();
         const successMsg = `${file.name} removed successfully.`
          Toastify({
            text: successMsg,
            duration: -1,
            close: true,
            gravity: "top",
            position: "right",
            style: {
              background: "#45425a",
              fontFamily: "'Josefin Sans', sans-serif",
              color: "#fefefe",
            },
          }).showToast();
       }, 
       error: function(error) {
         displayAJAXErrorMessage(error.status);
       }
     });
  },
  init: function () {
    userId = $("#user_id_2").val();

    const submitBtn = $("#audio_submit_btn");

    const dropZoneInstance = this;
    
    /* Fetch tracks if already uploaded by user and display in 
    dropzone window. */
    fetch(`/profile/get_users_tracks/${userId}`)
    .then((res) => { return res.json()})
    .then((data) => {
      let files = data.track_list;
      files.forEach((file) => {
        let mockFile = file
        let callback = null;
        let crossOrigin = null;
        let resizeThumbnail = true;
        dropZoneInstance.displayExistingFile(
          mockFile,
          "/media/audio-icon.png",
          callback,
          crossOrigin,
          resizeThumbnail
        );
      })
    })
    

    submitBtn.on("click", function () {
      console.log("click")
      dropZoneInstance.processQueue();
    });

    dropZoneInstance.on("processing", function (file) {
      console.log("processing");
      console.log(dropZoneInstance)
    });


    dropZoneInstance.on("success", function() {
      $.ajax({
        type: "GET",
        url: `/profile/upload_audio/${userId}`,
        success: function (res) {
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
            $("#add_audio_container").addClass("hidden");
            $("#calendar_container").removeClass("hidden");
            $("#second_breadcrumb").addClass("fill-breadcrumb")
            $("#second_breadcrumb_sm").addClass("fill-breadcrumb-sm")
            $("#second_breadcrumb_icon").addClass("fill-breadcrumb-icon-sm")
            $("#second_breadcrumb_text").addClass("dark-text")
            $(".edit_profile_header").html("Your Availability")

            const pageThreeText = `
                <div class="profile-prompt-lead text-center">
                    <p>Finding a dep is quicker and easier if you know if they are available on the day of your gig.</p>
                    <p>Add the dates when you are unavailable to make the depping process as smooth as possible.</p>
                </div>
            `;

            $(".profile-prompt-lead").html(pageThreeText)


          }, 1500)
        },
      }); 


    })
  },
};

const availabilityHeader = "Your Availability";
const avaliabilityLead = `<div class="profile-prompt-lead text-center">
                            <p>Finding a dep is quicker and easier if you know if they are available on the day of your gig.</p>
                            <p>Add the dates when you are unavailable to make the depping process as smooth as possible.</p>
                          </div>
                          `

$("#skip_audio_form").click({
  param1: "#add_audio_container",
  param2: "hidden",
  param3: "#calendar_container",
  param4: $(".edit_profile_header"),
  param5: $(".profile-prompt-lead"),
  param6: availabilityHeader,
  param7: avaliabilityLead
}, switchStep)

$("#skip_calendar_form").click({
  param1: "#calendar_container"
}, switchStep)



// Skip to Unavailability Calendar
function switchStep(event) {
    const el1 = $(event.data.param1);
    const el2 = $(event.data.param3);
    console.log(el1.attr("id"))

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
      window.location.href = "/"
    }
}

function changeHeader(headerEl, leadEl, header, lead) {
  const el1 = headerEl;
  const el2 = leadEl;

  const headerContent = header;
  const leadContent = lead;

  el1.html(headerContent)
  el2.html(leadContent)
}

// Displays a Toast with error message in case of AJAX errors
  function displayAJAXErrorMessage(status) {
      if (status === 0) {
        errorMsg = "Cannot connect, please make sure you are connected";
      } else if (status === 404) {
        errorMsg = `${status} error. We apologize; the resource was not found.`;
      } else if (status === 500) {
        errorMsg = `${status} error. We apologize. There is an internal server error.`;
      } else {
        errorMsg =
          "We apologize, there has been an error. We are working hard to rectify this.";
      }

      Toastify({
        text: errorMsg,
        duration: 10000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
          background: "#ff7086",
          fontFamily: "'Oxygen', sans-serif",
          color: "#202020",
        },
      }).showToast();
  }