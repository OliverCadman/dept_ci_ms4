$(document).ready(function() {
    /* Populates Job Detail Modals with data from Job Detail Cards
    
    Content is passed through the data attributes of "View Details" button
    and appended as html to the elements with relevant ID attributes.
    */
    $(".job_detail_btn").click(function() {
        $("#job_title").html($(this).data("job-title"));
        $("#event_name").html($(this).data("event-name"));
        $("#artist_name").html($(this).data("artist-name"));
        $("#event_city").html($(this).data("event-city"));
        $("#event_country").html($(this).data("event-country"));
        $("#fee").html(`£${$(this).data("job-fee")}`);
        $("#job_poster").html($(this).data("job-poster"));
        $("#job_description").html($(this).data("job-description"));
        $("#job_poster").html(
          `Posted by <a href="/profile/${$(this).data("job-poster")}" class="primary_font med_size">${$(this).data("job-poster")}</a>`);
        $("#register_interest_btn").attr(
          "href", `/jobs/register_interest/${$(this).data("job-id")}/${$(this).data("request-user")}`);

        if ($(this).data("job-poster-image")) {
            $("#poster_profile_img_wrapper").html(
              `<img src="${$(this).data("job-poster-image")}"
              alt="Image of Job Advertiser"
              width="75"
              height="75"
              class="modal_profile_image_thumbnail">`
            );
        } else {
            $("#poster_profile_img_wrapper").html(
              `<img src="/media/dept-logo.webp"
              alt="Image of Job Advertiser"
              width="75"
              height="75"
              class="modal_profile_image_thumbnail">`
            );
        }
        
    });
});