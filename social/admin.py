from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "date_of_message",)

admin.site.register(Message, MessageAdmin)
