"""
Registers various :mod:`~django.contrib.admin` models to generate the app's
admin site interface.

References
----------
* `The Django admin site`_

.. _The Django admin site:
   https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
"""

from django.contrib import admin
from django_mri.models.scan import Scan


class ScanAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.scan.Scan` to the admin interface.
    """

    #: Fields displayed on the change list page of the admin.
    list_display = (
        "id",
        "subject",
        "time",
        "number",
        "description",
    )

    #: List ordering in the Django admin views.
    ordering = ("subject", "time", "number")


admin.site.register(Scan, ScanAdmin)
