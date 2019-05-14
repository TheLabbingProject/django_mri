from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin
from django_dicom.models import Series
from django_mri.forms import ScanReview
from django_mri.models import Scan


class CreateScanView(CreateView, ModelFormMixin, LoginRequiredMixin):
    model = Scan
    form_class = ScanReview
    success_url = "/data_review/"
    template_name = "django_mri/scan/create_scan.html"


class CreateScanFromDicom(CreateScanView):
    def get_context_data(self, **kwargs):
        series = Series.objects.get(id=self.kwargs.get("pk"))
        self.object = Scan(dicom=series)
        self.object.update_fields_from_dicom()
        return super().get_context_data(**kwargs)

