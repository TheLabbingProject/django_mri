from django.urls import path, include
from django_mri import views
from rest_framework import routers

app_name = "mri"
router = routers.DefaultRouter()
router.register(r"scan", views.ScanViewSet)
router.register(r"nifti", views.NiftiViewSet)
router.register(r"sequence_type", views.SequenceTypeViewSet)
router.register(r"tree/unreviewed_dicom_patients", views.UnreviewedDicomPatientViewSet)
router.register(r"tree/unreviewed_dicom_series", views.UnreviewedDicomSeriesViewSet)


urlpatterns = [
    path("mri/", include(router.urls)),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
