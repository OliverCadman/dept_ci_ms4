/*
Handle removal of notification drop notification dropdown.
    
Functions:

getCookie() - Used to grab CSRFToken cookie from the browser,
              to add as a header in XMLHttpRequest.

            Params: 

            name - The name of the cookie to return.
                    In this case; "csrftoken"
    
removeNotification() - Opens an XMLHttpRequest to URL passed
                        in as an argument. If status is 200,
                        refresh the page. If error, display a toast
                        informing user of error.
                

            Params:

            removeNotificationURL - The URL of the XMLHttpRequest;
                                    ("{% url "remove_notification" notification.pk %} ")

            redirectURL - The redirect URL upon successful removal of notification.
                          ("{{ request.path }}")

Code referenced from YouTube tutorial:

Title: Building a Social Media App With Python 3 and Django: Part 12 User Notifications
Uploader: Legion Script
https://www.youtube.com/watch?v=_JKWYkz597c&t=889s
*/

// Function referenced from Django Documentation
// https://docs.djangoproject.com/en/4.0/ref/csrf/
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Open an XMLHttpRequest
function removeNotification(removeNotificationURL, redirectURL) {
  const csrfToken = getCookie("csrftoken");
  let xmlHttp = new XMLHttpRequest();

  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.readyState === XMLHttpRequest.DONE) {
      if (xmlHttp.status === 200) {
        window.location.replace(redirectURL);
      } else {
        const errorMsg = "Sorry, there was an error. Please try again";
        Toastify({
          text: errorMsg,
          duration: 5000,
          close: true,
          gravity: "top",
          position: "right",
          style: {
            background: "#ff7086",
            fontFamily: "'Oxygen', sans-serif",
            color: "#202020",
          },
        }).showToast();
      }
    }
  };

  xmlHttp.open("DELETE", removeNotificationURL, true);
  xmlHttp.setRequestHeader("X-CSRFToken", csrfToken);
  xmlHttp.send();
};