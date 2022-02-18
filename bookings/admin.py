from django.contrib import admin
from .models import Invitation

class InvitationAdmin(admin.ModelAdmin):

    list_display = ("invitation_number", "invite_sender",
                    "invite_receiver")

# Register your models here.
admin.site.register(Invitation, InvitationAdmin)

