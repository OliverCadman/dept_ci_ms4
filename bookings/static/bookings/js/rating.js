$(document).ready(function() {
    /*
      Allows clickability of star icons when leaving a rating with a review.
      The star className default to outlined stars on page load.

      All star icons are grabbed from the DOM, added to the ratingStarArray,
      mapped, and assigned a click event.
      The index of each icon element is assigned to the variable "i",
      to keep track of which icon along the row of icons has been clicked.
    
    */
    const ratingStars = document.getElementsByClassName("rating_star");

    const ratingStarArray = []

    for (let star of ratingStars) {
        ratingStarArray.push(star)
    }

    leaveStarRating(ratingStarArray);

    function leaveStarRating(starIcons) {
        const activeStarIcon = "rating_star fas fa-star"
        const inactiveStarIcon = "rating_star far fa-star"
        const lengthOfStars = starIcons.length
  
        starIcons.map((star) => {
            star.addEventListener("click", function() {

                // Keep track of index of clicked star
                let i = starIcons.indexOf(star);
                let starRating = i + 1;
                
                if (star.className === inactiveStarIcon) {
                  
                  // Decremental for loop enables all star icons up-to and including
                  // clicked star icon to be filled in, and "active".
                  for (i; i < lengthOfStars; i--) {
                    starIcons[i].className = activeStarIcon;
                  }
                } else {
                  // Incremental for loop enables all active star icons following
                  // and including clicked star icon to be outlined, and "inactive".
                  for (i; i < lengthOfStars; i++) {
                    starIcons[i].className = inactiveStarIcon;
                  }
                }
            })         

        
        });
    }    
})