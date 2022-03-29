from django.contrib import admin
from .models import (UserProfile, AudioFile, Equipment,
                     Instrument, UnavailableDate, Genre)


class UserEquipmentInline(admin.TabularInline):
    """
    Display User's Equipment Fields
    inline on UserProfile model.
    """
    model = Equipment


class UserProfileAdmin(admin.ModelAdmin):
    """
    Customize the layout and field display
    of the UserProfile model, and add
    the UserEquipmentInline class
    to display user's equipment in model.
    """
    inlines = [UserEquipmentInline]
    list_display = ["first_name", "user"]
    raw_id_fields = ["user"]
    readonly_fields = ("pk",)


class EquipmentAdmin(admin.ModelAdmin):
    """
    Customize the layout and field display of
    the Equipment model.
    """
    list_display = ("equipment_name", "related_user")


# Register the profiles app models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AudioFile)
admin.site.register(Instrument)
admin.site.register(UnavailableDate)
admin.site.register(Genre)
admin.site.register(Equipment, EquipmentAdmin)
