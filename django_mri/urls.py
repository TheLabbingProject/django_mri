from django.urls import path, include
from django_mri import views

app_name = "django_mri"
urlpatterns = [
    path("scan/upload/", views.DataUploadView.as_view(), name="scan_upload"),
    path("scan/create/", views.CreateScanView.as_view(), name="scan_create"),
    path(
        "scan/create/from_dicom/<int:pk>/",
        views.CreateScanFromDicom.as_view(),
        name="scan_create_from_dcm",
    ),
    path("dicom/", include("django_dicom.urls", namespace="dicom")),
]

