from django.contrib import admin
from .models import (UserProfile, AudioFile, Equipment,
                    Instrument, UnavailableDate, Genre)


class EquipmentAdmin(admin.ModelAdmin):

    list_display = ("equipment_name", "related_user")




# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AudioFile)
admin.site.register(Instrument)
admin.site.register(UnavailableDate)
admin.site.register(Genre)
admin.site.register(Equipment, EquipmentAdmin)

