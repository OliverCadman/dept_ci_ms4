$(document).ready(function() {
   document.querySelectorAll(".checkout-portal").forEach(function() {
     $(function() {
         fetch("config")
         .then((res) => { return res.json(); })
         .then((data) => {
            console.log(data)
           
         })
     })
   })
})




                

