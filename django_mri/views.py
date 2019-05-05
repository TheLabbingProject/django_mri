import django_dicom.data_import

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.generic.edit import ModelFormMixin
from django_dicom.models import Series
from django_mri.forms import ScanReview, ScanUpload
from django_mri.models import Scan


class CreateScanView(CreateView, ModelFormMixin, LoginRequiredMixin):
    model = Scan
    form_class = ScanReview
    success_url = "/mri/scan/upload/"
    template_name = "django_mri/scan/create_scan.html"

    def get_context_data(self, **kwargs):
        kwargs["new_dicoms"] = Scan.objects.get_orphan_dicom_series()
        return super().get_context_data(**kwargs)


class CreateScanFromDicom(CreateScanView):
    def get_context_data(self, **kwargs):
        series = Series.objects.get(id=self.kwargs.get("pk"))
        self.object = Scan(dicom=series)
        self.object.update_fields_from_dicom()
        kwargs["new_dicoms"] = Scan.objects.get_orphan_dicom_series()
        return super().get_context_data(**kwargs)


class DataUploadView(View):
    def get(self, request):
        dicoms = Scan.objects.get_orphan_dicom_series()
        return render(
            self.request, "django_mri/scan/upload_scan.html", {"new_dicoms": dicoms}
        )

    def post(self, request):
        form = ScanUpload(self.request.POST, self.request.FILES)
        if form.is_valid():
            image_file = self.request.FILES["file"]
            if image_file.name.endswith(".dcm"):
                importer = django_dicom.data_import.ImportImage(image_file)
                image, created = importer.run()
            elif image_file.name.endswith((".nii", ".nii.gz")):
                print("Add nifti handler")
            data = {"is_valid": True}
        else:
            data = {"is_valid": False}
        return JsonResponse(data)
