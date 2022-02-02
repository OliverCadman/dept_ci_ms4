from django.http import HttpResponse


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic webhook event
        """

        return HttpResponse(
            content=f"Webhook received: {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook
        """
        return HttpResponse(
            content=f"Payment intent succeeded: {event['type']}"
        )

    def handle_payment_intent_requires_payment_method(self, event):

        return HttpResponse(
            content=f"Action needed: {event['type']}"
        )