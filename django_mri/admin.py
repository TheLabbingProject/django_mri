from django.contrib import admin
from django_mri.models.scan import Scan


class ScanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "time",
        "number",
        "description",
    )
    ordering = ("subject", "time", "number")


admin.site.register(Scan, ScanAdmin)
