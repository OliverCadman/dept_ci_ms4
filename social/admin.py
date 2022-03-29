from django.contrib import admin
from .models import Message, Notification

"""
Admin config for the Social App
"""


class MessageAdmin(admin.ModelAdmin):
    """
    Customize list display of message objects
    """
    list_display = ("__str__", "date_of_message",)

admin.site.register(Message, MessageAdmin)
admin.site.register(Notification)
