$(document).ready(function() {
  /* Disable Travel and Backline Input Elements by Default, until
       the relative checkboxes are clicked */
  $("#id_backline_info").prop("disabled", true);
  $("#id_travel_info").prop("disabled", true);

  // Handle travel-provided-checkbox when checked */
  const travelProvidedCheckbox = $("#id_travel_provided");
  travelProvidedCheckbox.change(
    {
      elementId: "#id_travel_info",
    },
    function (e) {
      toggleDisableFormEl($(this), e.data.elementId);
    }
  );

  // Handle backline-provided-checkbox when checked
  const backlineProvidedCheckbox = $("#id_backline_provided");
  backlineProvidedCheckbox.change(
    {
      elementId: "#id_backline_info",
    },
    function (e) {
      toggleDisableFormEl($(this), e.data.elementId);
    }
  );

  function toggleDisableFormEl(togglerEl, elementId) {
    /* Toggle disabled attributes of input elements
           when checkbox state changes */

    let toggler = togglerEl;
    let elementToDisable = $(elementId);

    if (!toggler.attr("checked")) {
      toggler.attr("checked", true);
      elementToDisable.prop("disabled", false);
    } else {
      toggler.attr("checked", false);
      elementToDisable.prop("disabled", true);
    }
  }
})