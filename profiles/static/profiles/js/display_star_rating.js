$(document).ready(function() {
    /*
    Displays FontAwesome star icons proportionate to the rating number
    of each review (ranging from 0-5).

    If a user has been given a rating of 3 out of 5, this is represented
    by three filled star icons, and two outlined star icons.
    */

    // Grab the values of all ratings stored in hidden inputs
    let hiddenRatingInputs = [...document.getElementsByClassName("review_rating_no")];
    for (let i = 0; i < hiddenRatingInputs.length; i++) {
       let maxRating = 5;
       let rating = parseInt(hiddenRatingInputs[i].value);

       // Traverse DOM to find the star_rating_wrapper relative to each input in the loop.
       let starRatingWrapper = hiddenRatingInputs[i].parentElement.children[1]
       console.log(starRatingWrapper)
        
       // Create filled FontAwesome stars for each point of rating
       for (let k = 0; k < rating; k++) {
           let icon = document.createElement("i");
           icon.className = "rating_star fas fa-star";
           starRatingWrapper.appendChild(icon);
       }

       // If any points remain, the difference is represented by outlined stars.
       if (rating < maxRating) {
         let rateDelta = maxRating - rating;
         for (let j = 0; j < rateDelta; j++) {
             let icon = document.createElement("i");
             icon.className = "rating_star far fa-star";
             starRatingWrapper.appendChild(icon);
         }
       }
    }

    /*
    Represent the average rating using FontAwesome stars. The same method applies;
    get the average rating and number of reviews from json_script tags, and represent
    the average rating with a relative number of filled stars, leaving the remainder
    (out of 5) as outlined stars.
    */ 

    
    // Grab values from json_script
    const currentPath = window.location.href
    const endPoint = currentPath.split("/")[3]
    console.log(endPoint)
    if (endPoint === "profile") {
         let averageRating =
           document.getElementById("average_rating").textContent;
         const starIconContainers =
           document.getElementsByClassName("header_star_icons");

         // Loop through both containers (one for mobile, one for larger screens)
         for (container of starIconContainers) {
           let maxRating = 5;
           averageRating = parseInt(averageRating);
           let rateDelta = maxRating - averageRating;

           // Create filled FontAwesome star icons from average rating
           for (let i = 0; i < averageRating; i++) {
             let filledStarIcon = document.createElement("i");
             filledStarIcon.className = "rating_star fas fa-star";
             container.appendChild(filledStarIcon);
           }

           // Create FontAwesome outlined stars for remainder
           for (let j = 0; j < rateDelta; j++) {
             let outlinedStarIcon = document.createElement("i");
             outlinedStarIcon.className = "rating_star far fa-star";
             container.appendChild(outlinedStarIcon);
             container.appendChild;
           }

           // Get the number of reviews from json_script.
           // Display the number of reviews next to the average star rating.
           let numOfReviews =
             document.getElementById("num_of_reviews").textContent;
           let numOfReviewsDisplay = document.createElement("span");
           numOfReviewsDisplay.textContent = `(${numOfReviews})`;
           numOfReviewsDisplay.className = "secondary_font white_font ms-1";
           container.appendChild(numOfReviewsDisplay);
         }
    } else {
        
    }
   

})