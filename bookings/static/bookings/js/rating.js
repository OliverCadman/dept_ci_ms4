$(document).ready(function() {
    /*
      Allows clickability of star icons when leaving a rating with a review.
      The star className default to outlined stars on page load.

      All star icons are grabbed from the DOM, added to the ratingStarArray,
      mapped, and assigned a click event.
      The index of each icon element is assigned to the variable "i",
      to keep track of which icon along the row of icons has been clicked.
    
    */
    const ratingStars = [...document.getElementsByClassName("rating_star_review_modal")];
    const ratingDisplayEl = document.getElementsByClassName("rating_display")[0];
    ratingDisplayEl.textContent = "0/5";
    let activeClass = "rating_star rating_star_review_modal fas fa-star";
    let inactiveClass = "rating_star rating_star_review_modal far fa-star";

    leaveStarRating(ratingStars, ratingDisplayEl, activeClass, inactiveClass);

    const ratingStarsEdit = [...document.getElementsByClassName("rating_star_edit_review_modal")];
    const ratingDisplayElEdit = document.getElementsByClassName("rating_display")[1];
    ratingDisplayElEdit.textContent = "0/5";
    const activeClassEdit = "rating_star rating_star_edit_review_modal fas fa-star";
    const inactiveClassEdit = "rating_star rating_star_edit_review_modal far fa-star";

    leaveStarRating(ratingStarsEdit, ratingDisplayElEdit, activeClassEdit, inactiveClassEdit);

    function leaveStarRating(starIcons, ratingDisplayEl, activeClass, inactiveClass ) {
        const activeStarIcon = activeClass;
        const inactiveStarIcon = inactiveClass;
        const lengthOfStars = starIcons.length;
        let i;
        starIcons.map((star) => {
            star.addEventListener("click", function() {

                // Keep track of index of clicked star
                i = starIcons.indexOf(star);

                // Override zero-indexing to accurately represent number
                // of active stars.
                let starRating = i + 1;
                
                if (star.className.indexOf(inactiveStarIcon) !== -1) {

                    // Update the text content of rating/5 with new rating number.
                    displayRatingNumber(ratingDisplayEl, starRating);

                    // Decremental for loop enables all star icons up-to and including
                    // clicked star icon to be filled in, and "active".
                    for (i; i >= 0; i--) {
                        starIcons[i].className = activeStarIcon;
                    }
                } else {

                    // Update the text content of rating/5 with new rating number.
                    // Variable "i" passed in instead of "starRating" as zero-indexing required.
                    displayRatingNumber(ratingDisplayEl, i);

                    // Incremental for loop enables all active star icons following
                    // and including clicked star icon to be outlined, and "inactive".
                    for (i; i < lengthOfStars; i++) {
                        starIcons[i].className = inactiveStarIcon;
                    }
                }
            })         

        
        });
    }
    
    function displayRatingNumber(ratingEl, number) {
        console.log(number)
        // Update span element with new rating (out of 5)
        ratingEl.textContent = `${number}/5`;

        if (!ratingEl.classList.contains("edit_review_modal")) {
                const ratingInput = document.getElementById("id_rating");
                ratingInput.value = number;
                console.log(ratingInput);
                console.log(ratingInput.value)
        } else {
            const ratingInputEditReview = document.getElementById("edit_review_modal_rating");
            ratingInputEditReview.value = number;
            console.log(ratingInputEditReview);
            console.log(ratingInputEditReview.value);
        }
    }
})