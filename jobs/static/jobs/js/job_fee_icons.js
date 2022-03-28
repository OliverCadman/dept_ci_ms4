$(document).ready(function(){
    /* Translate the fees for each job into icons representing how
    lucrative a job is. For instance, a £50-£100 job will render one pound sign,
    £100-£200 two pound signs, £200-£300 3 pound signs etc. */

    // Grab the hidden inputs placed inside cards.
    let hiddenInputs = document.getElementsByClassName("hidden_fee_input");

    // Grab the input values and the parent div to hold the icon wrapper
    for (let input of hiddenInputs) {
        let hiddenInputVal = parseInt(input.value);
        let iconContainer = input.parentElement;

        // Create wrapper to hold icons
        let iconWrapper = document.createElement("div");
        let iconCount;

        // Assign icon count relative to each tier of fee
        if (1 <= hiddenInputVal && hiddenInputVal <= 100) {
            iconCount = 1;
        } else if (101 <= hiddenInputVal && hiddenInputVal <= 200) {
            iconCount = 2;
        } else if (201 <= hiddenInputVal && hiddenInputVal <= 300) {
            iconCount = 3;
        } else if (301 <= hiddenInputVal && hiddenInputVal <= 500) {
            iconCount = 4;
        } else {
            iconCount = 5;
        }

            /* Loop over the icon count and append icon to wrapper,
            based on value determined by the range of hidden input values.
            
            Finally, append the wrapper to the parent container.
            */
        for (let i = 0; i < iconCount; i++ ){
            let icon = document.createElement("i");
            icon.className = "<i class='fa-solid fa-dollar-sign job_fee_icon'></i>";
            if (iconCount === 1) {
                iconWrapper.appendChild(icon);
            } else if (iconCount === 2) {
                iconWrapper.appendChild(icon);
            } else if (iconCount === 3) {
                iconWrapper.appendChild(icon);
            } else if (iconCount === 4) {
                iconWrapper.appendChild(icon);
            } else if (iconCount === 5) {
                iconWrapper.appendChild(icon);
            }

            iconContainer.appendChild(iconWrapper);
        }
    }

});