/* Dropzone JS

Creates a new Dropzone instance, to allow for drag and drop of audio files
on the website's 'Edit Profile' page.

https://docs.dropzone.dev/
*/

const dropZone = (Dropzone.options.audioDropzone = {
    autoProcessQueue: true,
    // 30MB 
    maxFilesize: 30,
    clickable: true,
    uploadMultiple: true,
    // Remove tracks if necessary
    addRemoveLinks: true,
    acceptedFiles: ".mp3,.mp4,.m4a,.wav,.aac,.flac",
    maxFiles: 5,
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
    `
});

    
        