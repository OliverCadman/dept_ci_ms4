$(document).ready(function() {
    username = $("#user_name").val()

    $("#edit_profile_form").on("submit", function(e) {
       e.preventDefault()
       const url = `/profile/edit_profile/${username}`;
       $.ajax({
         type: "POST",
         url: url,
         data: {
           csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
           first_name: $("#id_first_name").val(),
           last_name: $("#id_last_name").val(),
           city: $("#id_city").val(),
           country: $("#id_country").val(),
           instruments_played: $("#id_instruments_played option:selected").val(),
           genres: $("#id_genres option:selected").val(),
           equipment_name: $("#id_equipment_name").val(),
           user_info: $("#id_user_info").val(),
           action: "post",
         },
         success: function (res) {
           console.log(res.success)
            if (res.success) {
              $("#edit-profile-form-container").addClass("hide-container")
              $("#add-audio-container").removeClass("hide-container")
            }
         },
       }); 
    })
})