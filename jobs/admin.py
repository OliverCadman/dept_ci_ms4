from django.contrib import admin

from .models import Job

class JobAdmin(admin.ModelAdmin):

    readonly_fields = ("pk",)

# Register your models here.
admin.site.register(Job, JobAdmin)