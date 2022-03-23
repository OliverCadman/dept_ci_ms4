$(document).ready(function () {
  /*
    JavaScript code prevents all fields being added as query params
    to the URL, therefore allowing for filtering/searching on a one-by-one
    basis.

    Disables each field if they fulfill condition (unchecked checkbox
    disables "available_today" field, empty "city" searchbox value disables
    field, etc.)

    */

  // Modify the value of the "Available Today" checkbox to "true" if checked.
  $("#available_today_checkbox").change(function () {
    if (this.checked) {
      $(this).val("true");
    }
  });

  // Allows for the checkbox to remain checked upon page refresh, if checked
  // by the user to search for a member who is "Available Today".
  if ($("#available_today_checkbox").val() == "true") {
    $("#available_today_checkbox").prop("checked", true);
  }

  // Checks the values of all fields in filter form.
  // Disables the unused fields upon submission of form.
  function checkForUnusedFilterFields() {
    if ($("#city").val() == "") {
      $("#city").prop("disabled", true);
    }

    if ($("#instrument_filter").val() == "all") {
      $("#instrument_filter").prop("disabled", true);
    }

    if ($("#available_today_checkbox").val() == "false") {
      $("#available_today_checkbox").prop("disabled", true);
    } else {
      $("#available_today_checkbox").checked;
    }

    if($("#genre").val() == "all") {
        $("#genre").prop("disabled", true);
    } 

    if($(".sort_selector").val() == "reset") {
      $(".sort_selector").prop("disabled", true);

    } else {

      let selector = $(".sort_selector");
      let currentUrl = new URL(window.location);

      let selectedVal = selector.val();
      console.log(selectedVal)

      if (selectedVal != "reset") {
        let sortCriteria = selectedVal.split("_")[0];
        let sortDirection = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sortCriteria);
        currentUrl.searchParams.set("direction", sortDirection);

        window.location.replace(currentUrl);
      } 
    }
  }

  $("#instrument_filter_form").on("submit", checkForUnusedFilterFields);
});
