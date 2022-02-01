from django.contrib import admin
from .models import (UserProfile, AudioFile, 
                    Instrument, UnavailableDate)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AudioFile)
admin.site.register(Instrument)
admin.site.register(UnavailableDate)

