from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, View
from django_mri.forms import ScanReview, ScanUpload
from django_mri.models import Scan


class CreateScanView(CreateView, LoginRequiredMixin):
    model = Scan
    form_class = ScanReview
    template_name = "django_mri/scan/create_scan.html"

    # def get_context_data(self, **kwargs):
    #     kwargs["new_dicoms"] = Scan.objects.get_orphan_dicom_series()
    #     return super().get_context_data(**kwargs)

    # def post(self, request):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():
    #         files = request.FILES.getlist("dcm_files")
    #         for file in files:
    #             if file.name.endswith(".dcm"):
    #                 Image.objects.from_dcm(file)
    #             elif file.name.endswith(".zip"):
    #                 Image.objects.from_zip(file)
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


class DataUploadView(View):
    def get(self, request):
        dicoms = Scan.objects.get_orphan_dicom_series()
        return render(
            self.request, "django_mri/scan/upload_scan.html", {"new_dicoms": dicoms}
        )

    # def post(self, request):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():
    #         files = request.FILES.getlist("dcm_files")
    #         for file in files:
    #             if file.name.endswith(".dcm"):
    #                 Image.objects.from_dcm(file)
    #             elif file.name.endswith(".zip"):
    #                 Image.objects.from_zip(file)
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def post(self, request):
        form = ScanUpload(self.request.POST, self.request.FILES)
        if form.is_valid():
            print(self.request.FILES)
            data = {"is_valid": True}
            # if
            # image = form.save()
            # data = {"is_valid": True, "name": photo.file.name, "url": photo.file.url}
        else:
            data = {"is_valid": False}
        return JsonResponse(data)
