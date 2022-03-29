from django.contrib import admin
from .models import Invitation, Booking, Review

from profiles.models import AudioFile


class AudioFileInline(admin.TabularInline):
    """
    Display audio files inline in their related
    Booking object.
    """

    model = AudioFile

    exclude = ("related_user",)


class BookingInline(admin.StackedInline):
    """
    Display bookings inline with their
    related Invitation object.
    """
    model = Booking


class InvitationAdmin(admin.ModelAdmin):
    """
    Customise display of model fields, and list
    display of each model instance.

    Add the BookingInline into Invitation
    Admin to view Booking Model alongside
    invitaiton model.
    """
    list_display = ("invitation_number", "invite_sender",
                    "invite_receiver",)

    readonly_fields = ("pk",)

    inlines = [BookingInline]


class BookingAdmin(admin.ModelAdmin):
    """
    Display Booking object's audio files
    inline with Booking object.
    """
    inlines = [AudioFileInline]

    readonly_fields = ("pk",)


class ReviewAdmin(admin.ModelAdmin):
    """
    Customise fields to display when
    Review was created.
    """
    readonly_fields = ("review_created",)


# Register models and model Admin.
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
