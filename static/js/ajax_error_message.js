// Displays a Toast with error message in case of AJAX errors
function displayAJAXErrorMessage(status) {
  if (status === 0) {
    errorMsg = "Cannot connect, please make sure you are connected";
  } else if (status === 404) {
    errorMsg = `${status} error. We apologize; the resource was not found.`;
  } else if (status === 500) {
    errorMsg = `${status} error. We apologize. There is an internal server error.`;
  } else {
    errorMsg =
      "We apologize, there has been an error. We are working hard to rectify this.";
  }

  Toastify({
    text: errorMsg,
    duration: 10000,
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
