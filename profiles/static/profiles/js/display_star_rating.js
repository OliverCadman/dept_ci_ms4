$(document).ready(function() {

  /*
  Display Star Ratings in User's Profile and Dashboard
  Page, along with the number of reviews a user has received.
  */ 

  /* URL information needed in order to render the icons
  relative to the styling and arrangement of elements on
  either page.
  
  */
  const currentPath = window.location.href;
  let endPoint = currentPath.split("/");

  const profileEndpoint = currentPath.split("/")[3]
  let variableEndpoint = currentPath.split("/")[4]

  endPoint = endPoint.slice(3).join("/");

  let hiddenRatingInputs = [
    ...document.getElementsByClassName("review_rating_no"),
  ];

  if (profileEndpoint && variableEndpoint !== "dashboard") {
    // If Profile Page
    displayStarRating(hiddenRatingInputs, 1, "white_font");
  } else {
    // If Dashboard Page
    displayStarRating(hiddenRatingInputs, 2)
  }

  function displayStarRating(hiddenRatingInputs, index, variableColour) {
    /*
    Displays FontAwesome star icons proportionate to the rating number
    of each review (ranging from 0-5).

    If a user has been given a rating of 3 out of 5, this is represented
    by three filled star icons, and two outlined star icons.
    */

    // Grab the values of all ratings stored in hidden inputs
    for (let i = 0; i < hiddenRatingInputs.length; i++) {
      let maxRating = 5;
      let rating = parseInt(hiddenRatingInputs[i].value);

      // Traverse DOM to find the star_rating_wrapper relative to each input in the loop.
      let starRatingWrapper = hiddenRatingInputs[i].parentElement.children[index]


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

    // Retrieve average rating from JSON script
    let averageRating = document.getElementById("average_rating").textContent;
    const starIconContainers =
      document.getElementsByClassName("star_icon_container");

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

      // Get the number of reviews from JSON Script.
      // Display the number of reviews next to the average star rating.
      let numOfReviews = document.getElementById("num_of_reviews").textContent;
      let numOfReviewsDisplay = document.createElement("span");


      if (numOfReviews > 0) {
        numOfReviewsDisplay.className = `secondary_font ${variableColour} ms-1 position-relative`;
        numOfReviewsDisplay.textContent = `(${numOfReviews})`;
      } else {
        numOfReviewsDisplay.className =
          "secondary_font white_font med_small_text position-relative";
        numOfReviewsDisplay.textContent = "No Reviews";
      }

      container.appendChild(numOfReviewsDisplay);
    }
  }
})