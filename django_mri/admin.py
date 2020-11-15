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
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_mri.models.data_directory import DataDirectory
from django_mri.models.scan import Scan
from django_mri.models.session import Session


SCAN_VIEW_NAME = "admin:django_mri_scan_change"
SCAN_LINK_HTML = html = '<a href="{url}">{text}</a>'


class ScanAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.scan.Scan` class to the admin
    interface.
    """

    #: Fields displayed on the change list page of the admin.
    list_display = (
        "id",
        "session",
        "time",
        "number",
        "description",
    )

    #: List ordering in the Django admin views.
    ordering = "session", "time", "number"


class ScanInline(admin.TabularInline):
    """
    Admin site *InLine* for the :class:`~django_mri.models.scan.Scan` model.
    """

    model = Scan
    fields = (
        "number_",
        "time",
        "description",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution_",
        "comments",
    )
    readonly_fields = (
        "number_",
        "time",
        "description",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution_",
    )
    ordering = ("number",)

    def spatial_resolution_(self, scan: Scan) -> str:
        """
        Returns a nicely formatted representation of the scan's spatial
        resolution.

        Parameters
        ----------
        scan : Scan
            Scan instance

        Returns
        -------
        str
            Formatted spatial resolution representation
        """

        try:
            return " x ".join(
                [f"{number:.2g}" for number in scan.spatial_resolution]
            )
        except TypeError:
            return ""

    def number_(self, scan: Scan) -> str:
        """
        Returns an HTML link to the scan instance's *change* view.

        Parameters
        ----------
        scan : Scan
            Scan instance

        Returns
        -------
        str
            HTML link
        """

        url = reverse(SCAN_VIEW_NAME, args=(scan.id,))
        link_html = SCAN_LINK_HTML.format(url=url, text=scan.number)
        return mark_safe(link_html)


class SessionAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.session.Session` model to the admin
    interface.
    """

    #: List the associated scan instances.
    inlines = (ScanInline,)

    #: Fields displayed on the change list page of the admin.
    list_display = (
        "id",
        "measurement",
        "subject",
        "time",
        "comments",
    )

    #: List ordering in the Django admin views.
    ordering = ("-time",)

    class Media:
        css = {"all": ("django_mri/css/hide_admin_original.css",)}


class DataDirectoryAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.data_directory.DataDirectory` model to
    the admin interface.
    """

    list_display = "id", "title", "description", "created", "modified"


admin.site.register(Scan, ScanAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(DataDirectory, DataDirectoryAdmin)
