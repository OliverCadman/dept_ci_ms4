$(document).ready(function() {
    /*
    Equipment Form - Text Input Addition
    
    Enables user to add more text input fields, should they need to
    list more than one item of equipment that they own.
    */ 
    const equipmentTextInput = $("#id_equipment_name")
    equipmentTextInput.addClass("equipment-text-input")

    const equipmentTextInputWrapper = $("#div_id_equipment_name")
    let faPlusIcon = document.createElement("i")

    faPlusIcon.classList.add("fas", "fa-plus-circle", "add-new-equipment-icon")
   

    equipmentTextInputWrapper.append(faPlusIcon)

    
    let idValue = 0;

    faPlusIcon.addEventListener("click", function(e) {
        idValue++

        const newId = "id_equipment_name_" + idValue
        const inputElement = document.createElement("input")
        inputElement.type = "text"
        inputElement.name = "equipment_name"
        inputElement.classList.add("textinput", "textInput", "form-control", "equipment-text-input")
        inputElement.required = true
        inputElement.id = `${newId}`
        
        equipmentTextInputWrapper.append(inputElement)
        equipmentTextInputWrapper.append(e.target)
        
    })
})