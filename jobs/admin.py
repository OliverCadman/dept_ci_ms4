from django.contrib import admin

from .models import Job


class JobAdmin(admin.ModelAdmin):
    """
    Customise object fields and
    list display of Job Objects.
    """
    readonly_fields = ("pk",)
    list_display = ("__str__", "is_taken", "confirmed_member",)

admin.site.register(Job, JobAdmin)
