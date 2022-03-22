    function displayToast(message, representativeColor) {
        Toastify({
          text: message,
          duration: -1,
          close: true,
          gravity: "top",
          position: "right",
          style: {
            background: "#fefefe",
            fontFamily: "'Josefin Sans', sans-serif",
            color: representativeColor,
            fontSize: "20px",
            maxWidth: "100%"
          },
        }).showToast();
      }
  
