    function displayToast(message) {
        Toastify({
          text: message,
          duration: -1,
          close: true,
          gravity: "top",
          position: "right",
          style: {
            background: "#202020",
            fontFamily: "'Josefin Sans', sans-serif",
            color: "#fefefe",
          },
        }).showToast();
      }
  
