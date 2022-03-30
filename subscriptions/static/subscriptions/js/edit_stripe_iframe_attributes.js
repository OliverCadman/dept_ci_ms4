$(document).ready(function () {
    /* 
    Edit the attributes of an auto-generated
    Stripe 'iframe' element, so as not to
    throw validation errors in the W3C HTML Markup Validator. 
    */

    $(document).ready(function () {
        const stripeIFrame = $("iframe");
        let stripeIFrameNameAttr = stripeIFrame.attr("name");
        stripeIFrameNameAttr = stripeIFrameNameAttr.split("_")[2];
        stripeIFrame.attr("name", stripeIFrameNameAttr);
        stripeIFrame.removeAttr("frameborder");
        stripeIFrame.removeAttr("allowtransparency");
        stripeIFrame.removeAttr("scrolling");
    });
})