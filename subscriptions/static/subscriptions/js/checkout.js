/*
Request to handle payment event when user chooses a subscription tier.
Fetches stripe public key and redirects to Stripe checkout if response 
is valid.

https://stripe.com/docs/js/checkout/redirect_to_checkout
*/

$(document).ready(function() {
   document.querySelectorAll(".checkout-portal").forEach(function() {
     $(function() {
         // Requests backend for stripe public key and returns result in json format
         fetch("/subscribe/config/")
         .then((res) => { 
            return res.json(); })
         .then((data) => {
             // Initialize Stripe object
             stripe = Stripe(data.public_key)

             /* Posts price_id data to be handled by checkout session 
             in the backend, and handles session ID from returned data
             to be allow for stripe checkout redirect. */
             $(".checkout-portal").click(function(e) {
                 const inputId = e.target.parentElement.children[1].id
                 if (inputId === "tier_one_price_id") {
                    $.post({
                      url: "/subscribe/checkout/",
                      data: {
                        price_id: $("#tier_one_price_id").val(),
                      },
                      success: (res) => {
                        return res;
                      },
                    }).then((data) => {
                      if (data.error) {
                          // TODO: Customise error handling
                        throw Error("An error has occurred!");
                      } else {
                        return stripe.redirectToCheckout({
                          sessionId: data.session_id,
                        });
                      }
                    });

                 } else {
                     $.post({
                       url: "/subscribe/checkout/",
                       data: {
                         price_id: $("#tier_two_price_id").val(),
                       },
                       success: (result) => {
                         return result;
                       },
                     }).then((data) => {
                       if (data.error) {
                        // TODO: Customise error handling
                         throw Error("An error has occurred!");
                       } else {
                         return stripe.redirectToCheckout({
                           sessionId: data.session_id,
                         });
                       }
                     });
                 }
             })
           
         })
     })
   })
})




                

