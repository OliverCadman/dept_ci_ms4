from django.contrib import admin
from .models import (UserProfile, AudioFile, Equipment,
                    Instrument, UnavailableDate, Genre)


class UserEquipmentInline(admin.TabularInline):
    model = Equipment


class UserAudioInline(admin.TabularInline):
    model = AudioFile


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserEquipmentInline]
    list_display = ["first_name", "user"]
    raw_id_fields = ["user"]
    readonly_fields = ("pk",)


class EquipmentAdmin(admin.ModelAdmin):

    list_display = ("equipment_name", "related_user")




# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AudioFile)
admin.site.register(Instrument)
admin.site.register(UnavailableDate)
admin.site.register(Genre)
admin.site.register(Equipment, EquipmentAdmin)

