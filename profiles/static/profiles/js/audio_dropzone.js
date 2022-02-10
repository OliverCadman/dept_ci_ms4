/* Dropzone JS

Creates a new Dropzone instance, to allow for drag and drop of audio files
on the website's 'Edit Profile' page.

https://docs.dropzone.dev/
*/
username = $("#user_name_2").val();

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
  init: function () {
    username = $("#user_name_2").val();

    const submitBtn = $("#audio_submit_btn");

    dropZoneInstance = this;

    submitBtn.on("click", function () {
      dropZoneInstance.processQueue();
    });

    dropZoneInstance.on("processing", function (file) {
      console.log("processing");
    });

    // dropZoneInstance.on("complete", function() {
    //     dropZoneInstance.removeFile(file);
    // })
  },
};
