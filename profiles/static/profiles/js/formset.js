/*
    Add extra text inputs dynamically in the 'Equipment List' fields, should the user need
    to add more items of equipment to be displayed.

    Referenced from YouTube tutorial:
    Title - Dynamic New Forms in a Django Formset Via JavaScript
    Uploader - CodingEntrepeneurs

    https://www.youtube.com/watch?v=s3T-w2jhDHE&list=PLEsfXFp6DpzRMby_cSoWTFw8zaMdTEXgL&index=64
*/

$(document).ready(function () {
  // ----- "Add More" Button Event Handlers -----

  // Equipment Form (Edit Profile Page)
  let addMoreBtn = document.getElementById("add_more_btn");

  if (addMoreBtn.classList.contains("equipment_form_btn")) {
    addMoreBtn.addEventListener("click", addMoreForms);
    addMoreBtn.copyTarget = "equipment_form_list";
    addMoreBtn.formCopyClass = "equipment_form";
    addMoreBtn.inputAttribute = "equipment_name";
    addMoreBtn.errorMessageContainer = "equipment_error_message";
  } else {
    addMoreBtn.addEventListener("click", addMoreForms);
    addMoreBtn.copyTarget = "audio_form_list";
    addMoreBtn.formCopyClass = "audio_form";
    addMoreBtn.inputAttribute = "audio_name";
    addMoreBtn.errorMessageContainer = "audiofile_error_message";
  }

  function addMoreForms(e) {
    e.preventDefault();

    // The div where the added input field will be appended
    const formCopyTarget = document.getElementById(e.currentTarget.copyTarget);
    const formCopyEmptyEl = document
      .getElementById("empty_form")
      .cloneNode(true);

    formCopyEmptyEl.setAttribute("class", e.currentTarget.formCopyClass);
    console.log(formCopyEmptyEl);

    // Hidden input field auto-generated by Django, to keep track of forms in model formset factory
    const totalForms = document.getElementById("id_form-TOTAL_FORMS");
    const currentForms = document.getElementsByClassName(
      e.currentTarget.formCopyClass
    );
    let currentFormCount = currentForms.length;
    formCopyEmptyEl.setAttribute(
      "id",
      `div_id_form-${currentFormCount}-${e.currentTarget.inputAttribute}`
    );
    totalForms.setAttribute("value", currentFormCount + 1);

    // Regex to update the new hidden input attributes when a new input field is added
    const regex = new RegExp("__prefix__", "g");
    formCopyEmptyEl.innerHTML = formCopyEmptyEl.innerHTML.replace(
      regex,
      currentFormCount
    );

    if (e.currentTarget.formCopyClass === "audio_form") {
      if (currentForms.length < 15) {
        formCopyTarget.append(formCopyEmptyEl);
      } else {
        let errorMessageContainer = document.getElementById(
          e.currentTarget.errorMessageContainer
        );
        let errorMessage = "You cannot add more than 15 files.";
        errorMessageContainer.innerText = errorMessage;
      }
    } else {
      if (currentForms.length < 5) {
        formCopyTarget.append(formCopyEmptyEl);
      } else {
        let errorMessageContainer = document.getElementById(
          e.currentTarget.errorMessageContainer
        );
        let errorMessage = "You cannot add more than 5 items."
        errorMessageContainer.innerText = errorMessage;
      }
    }
  }
});
