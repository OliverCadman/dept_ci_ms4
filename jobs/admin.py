from django.contrib import admin

from .models import Job


class JobAdmin(admin.ModelAdmin):

    readonly_fields = ("pk",)
    list_display = ("__str__", "is_taken", "confirmed_member",)

# Register your models here.
admin.site.register(Job, JobAdmin)
