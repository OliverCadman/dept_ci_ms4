$(document).ready(function () {
/* Cycles through the list of images displaying examples of website 
  usage, featured alongside the bulleted list in the "How DepT Works"
  section of the website's home page.
  */
  $(".benefits_gallery").each(function () {
      let carouselList = $(this);
      let activeItem = carouselList.find(">li.active");
      let carouselSpeed = 5000;
      setInterval(function () {

          // If last item is active, remove the class manually and add active class to
          // first item in carouselList.

          // If first item is active, then use jquery .next() to find next li element,
          // and add active class.
          if (activeItem.is(":last-child")) {
            activeItem.removeClass("active");
            activeItem = carouselList.find(">li:first-child");
            activeItem.addClass("active");
          } else {
            activeItem.removeClass("active");
            activeItem.next().addClass("active");
            activeItem = activeItem.next();
          }
      }, carouselSpeed);
  });
});