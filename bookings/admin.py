from django.contrib import admin
from .models import Invitation, Booking, Review

from profiles.models import AudioFile

class AudioFileInline(admin.TabularInline):

    model = AudioFile

    exclude = ("related_user",)


class BookingInline(admin.StackedInline):

    model = Booking


class InvitationAdmin(admin.ModelAdmin):

    list_display = ("invitation_number", "invite_sender",
                    "invite_receiver",)

    readonly_fields = ("pk",)

    inlines = [BookingInline]


class BookingAdmin(admin.ModelAdmin):
    inlines = [AudioFileInline]

    readonly_fields = ("pk",)

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ("review_created",)


# Register your models here.
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)

