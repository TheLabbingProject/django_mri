"""
Registers various :mod:`~django.contrib.admin` models to generate the app's
admin site interface.

References
----------
* `The Django admin site`_

.. _The Django admin site:
   https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
"""
from bokeh.embed import autoload_static
from bokeh.layouts import layout
from bokeh.resources import CDN
from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_analyses.models.run import Run
from nonrelated_inlines.admin import NonrelatedStackedInline

from django_mri.models.data_directory import DataDirectory
from django_mri.models.irb_approval import IrbApproval
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_mri.models.session import Session
from django_mri.utils import get_measurement_model
from django_mri.utils.html import Html

DOWNLOAD_BUTTON = '<span style="padding-left:20px;"><a href={url} type="button" class="button" id="{file_format}-download-button">{text}</a></span>'  # noqa: E501
SCAN_VIEW_NAME = "admin:django_mri_scan_change"
SCAN_LINK_HTML = '<a href="{url}">{text}</a>'
ZIP_VIEWS = {"dicom": "dicom:to_zip", "nifti": "mri:nifti_to_zip"}


def custom_titled_filter(title: str):
    """
    Copied from SO:
    https://stackoverflow.com/a/21223908/4416932
    """

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def create_scan_download_links(instance: Scan) -> str:
    links = ""
    # DICOM download link if associated Series instance exists.
    if instance.dicom:
        url = reverse("dicom:to_zip", args=(instance.dicom.id,))
        button = DOWNLOAD_BUTTON.format(
            url=url, file_format="dicom", text="DICOM"
        )
        links += button
    # NIfTI download link for non-localizer scans.
    if "loc" not in instance.description.lower():
        url = reverse("mri:nifti_zip", args=(instance.id,))
        button = DOWNLOAD_BUTTON.format(
            url=url, file_format="nifti", text="NIfTI"
        )
        links += button
    return mark_safe(links)


class ScanRunInline(NonrelatedStackedInline):
    model = Run
    fields = (
        "run_link",
        "analysis_version_link",
        "start_time",
        "end_time",
        "duration",
        "_status",
        "download",
    )
    readonly_fields = (
        "run_link",
        "analysis_version_link",
        "start_time",
        "end_time",
        "duration",
        "_status",
        "download",
    )
    can_delete = False
    extra = 0
    template = "admin/django_mri/scan/edit_inline/tabular.html"

    class Media:
        css = {"all": ("django_mri/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: Scan):
        return False

    def get_form_queryset(self, instance: Scan):
        return instance.query_run_set()

    def run_link(self, instance: Run) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    def analysis_version_link(self, instance: Run) -> str:
        model_name = instance.analysis_version.__class__.__name__
        pk = instance.analysis_version.id
        text = str(instance.analysis_version)
        return Html.admin_link(model_name, pk, text)

    def _status(self, instance: Run) -> bool:
        if instance.status == "SUCCESS":
            return True
        elif instance.status == "FAILURE":
            return False

    def download(self, instance: Run) -> str:
        if instance.status == "SUCCESS" and instance.path.exists():
            url = reverse("analyses:run_to_zip", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, file_format=f"run-{instance.id}", text="ZIP"
            )
            return mark_safe(button)
        return ""

    analysis_version_link.short_description = "Anaylsis Version"
    run_link.short_description = "Run"
    _status.boolean = True


class ScanAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.scan.Scan` class to the admin
    interface.
    """

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "session",
                    "number",
                    "description",
                    "time",
                    "echo_time",
                    "repetition_time",
                    "inversion_time",
                    "spatial_resolution",
                    "institution_name",
                    "comments",
                ]
            },
        ),
        (
            "File formats",
            {
                "fields": [
                    ("dicom_link", "is_updated_from_dicom"),
                    "nifti",
                    "mif",
                ]
            },
        ),
        ("Research", {"fields": ["study_groups"]}),
        (None, {"fields": ["added_by"]}),
    )

    #: Fields displayed on the change list page of the admin.
    list_display = (
        "id",
        "subject_link",
        "session_link",
        "number",
        "time",
        "description",
        "sequence_type",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution_",
        "comments",
        "download",
    )
    readonly_fields = (
        "dicom_link",
        "session_link",
        "spatial_resolution_",
        "nifti",
        "mif",
        "download",
        "sequence_type",
    )
    list_filter = (("dicom__sequence_type", admin.AllValuesFieldListFilter),)
    search_fields = ("id", "session__id", "description", "comments")
    inlines = (ScanRunInline,)

    class Media:
        js = ("//cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",)

    def change_view(
        self,
        request,
        object_id: int,
        form_url: str = "",
        extra_context: dict = None,
    ):
        return super().change_view(request, object_id, form_url, extra_context)

    def session_link(self, instance: Scan) -> str:
        model_name = instance.session.__class__.__name__
        pk = instance.session.id
        return Html.admin_link(model_name, pk)

    def subject_link(self, instance: Scan) -> str:
        model_name = instance.session.subject.__class__.__name__
        pk = instance.session.subject.id
        return Html.admin_link(model_name, pk)

    def dicom_link(self, instance: Scan) -> str:
        if instance.dicom:
            model_name = instance.dicom.__class__.__name__
            pk = instance.dicom.id
            link = Html.admin_link(model_name, pk)
            url = reverse("dicom:to_zip", args=(instance.dicom.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, file_format="dicom", text="Download"
            )
            return mark_safe(f"{link}{button}")

    def nifti(self, instance: Scan) -> str:
        if instance._nifti:
            model_name = instance.nifti.__class__.__name__
            pk = instance.nifti.id
            link = Html.admin_link(model_name, pk)
            url = reverse("mri:nifti_to_zip", args=(instance.nifti.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, file_format="nifti", text="Download"
            )
            return mark_safe(f"{link}{button}")

    def mif(self, instance: Scan) -> str:
        expected = instance.get_default_mif_path()
        if expected.exists():
            return str(expected)

    def download(self, instance: Scan) -> str:
        return create_scan_download_links(instance)

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

    session_link.short_description = "Session"
    subject_link.short_description = "Subject"
    dicom_link.short_description = "DICOM"


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
        "download",
    )
    readonly_fields = (
        "number_",
        "time",
        "description",
        "echo_time",
        "inversion_time",
        "repetition_time",
        "spatial_resolution_",
        "download",
    )
    ordering = ("number",)
    extra = 0
    can_delete = False

    def download(self, instance: Scan) -> str:
        return create_scan_download_links(instance)

    def has_add_permission(self, request, instance: Scan):
        return False

    def spatial_resolution_(self, instance: Scan) -> str:
        """
        Returns a nicely formatted representation of the scan's spatial
        resolution.

        Parameters
        ----------
        instance : Scan
            Scan instance

        Returns
        -------
        str
            Formatted spatial resolution representation
        """

        try:
            return " x ".join(
                [f"{number:.2g}" for number in instance.spatial_resolution]
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


class MeasurementDefinitionFilter(SimpleListFilter):
    title = "measurement definition"
    parameter_name = "measurement definition"

    def lookups(self, request, model_admin):
        sessions = (
            model_admin.model.objects.filter(measurement__isnull=False)
            .order_by("measurement__title")
            .distinct("measurement__title")
        )
        return [
            (session.measurement.id, session.measurement.title)
            for session in sessions
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(measurement=value)
        return queryset


class SessionAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.session.Session` model to the admin
    interface.
    """

    inlines = (ScanInline,)
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "subject",
                    "measurement",
                    "time",
                    "comments",
                    "irb",
                    "created",
                    "modified",
                    "download",
                ]
            },
        ),
    )
    list_display = (
        "id",
        "time",
        "subject_link",
        "measurement_link",
        "scan_count",
        "irb",
        "created",
        "comments",
        "download",
    )
    list_filter = (
        "time",
        MeasurementDefinitionFilter,
        ("irb", custom_titled_filter("IRB approval")),
        "created",
    )
    readonly_fields = (
        "created",
        "download",
        "modified",
    )
    search_fields = (
        "id",
        "subject__id_number",
        "subject__id",
        "irb__number",
        "comments",
    )
    actions = ("export_csv",)

    class Media:
        css = {"all": ("django_mri/css/hide_admin_original.css",)}

    @admin.action(description="Export CSV")
    def export_csv(self, request, queryset):
        df = queryset.to_dataframe()
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=sessions.csv"
            },
        )
        df.to_csv(path_or_buf=response)
        return response

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context
        )
        if hasattr(response, "context_data"):
            queryset = response.context_data["cl"].queryset
            if queryset.count() > 10:
                month_distribution_plot = queryset.plot_measurement_by_month()
                figure_layout = [month_distribution_plot]
                figure = layout(figure_layout)
                js, tag = autoload_static(figure, CDN, "tmp_bokeh_figure")
                extra_context = {"bokeh_tag": tag, "bokeh_js": js}
                response.context_data.update(extra_context)
        return response

    def get_form(self, request, instance, **kwargs):
        # Show only measurement definitions with the content_type set to
        # Session.
        form = super().get_form(request, instance, **kwargs)
        content_type = ContentType.objects.get_for_model(Session)
        MeasurementDefinition = get_measurement_model()
        queryset = MeasurementDefinition.objects.filter(
            content_type=content_type
        )
        form.base_fields["measurement"] = forms.ModelChoiceField(
            queryset=queryset
        )
        return form

    def download(self, instance: Session) -> str:
        links = ""
        url = reverse("mri:session_nifti_zip", args=(instance.id,))
        button = DOWNLOAD_BUTTON.format(
            url=url, file_format="nifti", text="NIfTI"
        )
        links += button
        first_scan = instance.scan_set.first()
        if first_scan.dicom:
            url = reverse("mri:session_dicom_zip", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, file_format="dicom", text="DICOM"
            )
            links += button
        return mark_safe(links)

    def subject_link(self, instance: Session) -> str:
        if instance.subject:
            model_name = instance.subject.__class__.__name__
            pk = instance.subject.id
            text = instance.subject.id_number
            return Html.admin_link(model_name, pk, text)

    def measurement_link(self, instance: Session) -> str:
        if instance.measurement:
            model_name = instance.measurement.__class__.__name__
            pk = instance.measurement.id
            text = instance.measurement.title
            return Html.admin_link(model_name, pk, text)

    def scan_count(self, instance: Session) -> int:
        return instance.scan_set.count()

    measurement_link.short_description = "Measurement Definition"
    subject_link.short_description = "Subject"


class NiftiAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.nifti.NIfTI` model to the admin
    interface.
    """

    fields = "path", "is_raw", "has_json"
    list_display = "id", "path", "scan_link"
    readonly_fields = "has_json", "path", "scan_link"

    def scan_link(self, instance: NIfTI) -> str:
        try:
            scan = Scan.objects.get(_nifti=instance)
        except Scan.DoesNotExist:
            pass
        else:
            return Html.admin_link("Scan", scan.id)

    def has_json(self, instance: NIfTI) -> str:
        return instance.json_file.exists()

    has_json.boolean = True
    scan_link.short_description = "Scan"


class DataDirectoryAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.data_directory.DataDirectory` model to
    the admin interface.
    """

    list_display = "id", "title", "description", "created", "modified"


class IrbApprovalAdmin(admin.ModelAdmin):
    """
    Adds the :class:`~django_mri.models.irb_approval.IrbApproval` model to
    the admin interface.
    """

    list_display = "id", "institution", "number", "document"


admin.site.register(DataDirectory, DataDirectoryAdmin)
admin.site.register(IrbApproval, IrbApprovalAdmin)
admin.site.register(NIfTI, NiftiAdmin)
admin.site.register(Scan, ScanAdmin)
admin.site.register(Session, SessionAdmin)
