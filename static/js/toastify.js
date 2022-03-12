    function displayToast(message, representativeBackground, representativeColor) {
        Toastify({
          text: message,
          duration: -1,
          close: true,
          gravity: "top",
          position: "right",
          style: {
            background: "#45425a",
            fontFamily: "'Josefin Sans', sans-serif",
            color: "#fefefe",
          },
        }).showToast();
      }
  
