$(document).ready(function() {
  console.log("ready");

  /* Delete Invitation Modal
      --------------------------------
       Grabs invitation as data-attribute passed through
       button to open confirmation modal, and sets the href attribute of
       link to delete invitation, with invitation ID appended.
       
       Passed into populateDeleteHrefAttribute function */

  $(".confirm_invite_delete_btn").click(function () {
    let deleteLink = "#confirm_invite_delete";
    let href = `/bookings/delete_invitation/${$(this).data("invitation-id")}`;

    populateDeleteHrefAttribute(deleteLink, href);
  });

  /* Delete Job Modal
      --------------------------------
       Grabs invitation as data-attribute passed through
       button to open confirmation modal, and sets the href attribute of
       link to delete invitation, with invitation ID appended.
       
       Passed into populateDeleteHrefAttribute function*/

  $(".confirm_job_delete_btn").click(function () {
    let deleteLink = "#confirm_job_delete";
    let href = `/jobs/delete_job/${$(this).data("job-id")}`;

    populateDeleteHrefAttribute(deleteLink, href);
  });

  /* Delete Profile Modal
      --------------------------------
       Grabs the profile ID as data-attribute passed through
       button to open confirmation modal, and sets the href attribute of
       link to delete profile, with profile ID appended.
       
       Passed into populateDeleteHrefAttribute function*/

  $(".confirm_profile_delete_btn").click(function () {
    let deleteLink = "#confirm_profile_delete";
    let href = `/profile/delete_account/${$(this).data("profile-id")}`;

    populateDeleteHrefAttribute(deleteLink, href);
  });

  function populateDeleteHrefAttribute(deleteLink, href) {
    console.log(deleteLink, href);
    /* 
        Dynamically alters the href attribute of anchor tag
        to delete an object.
        */
    $(deleteLink).attr("href", href);
  }
})