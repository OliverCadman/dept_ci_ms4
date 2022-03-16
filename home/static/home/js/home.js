$(document).ready(function () {
/* Cycles through the list of images displaying examples of website 
  usage, featured alongside the bulleted list in the "How DepT Works"
  section of the website's home page.
  */
  $(".cycle_gallery").each(function () {
      let carouselList = $(this);
      let activeItem = carouselList.find(">li.active");
      let carouselSpeed = 5000;
      setInterval(function () {

          // If last item is active, remove the class manually and add active class to
          // first item in carouselList.

          // If first item is active, then use jquery .next() to find next li element,
          // and add active class.
          (activeItem.is(":last-child")
            ? (activeItem.removeClass("active"),
              (activeItem = carouselList.find(">li:first-child").addClass("active")))
            : (activeItem.removeClass("active").next().addClass("active"),
              (activeItem = activeItem.next())))
      }, carouselSpeed);
  });
});