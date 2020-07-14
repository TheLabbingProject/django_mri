from django.urls import path, include
from django_mri import views
from rest_framework import routers

app_name = "mri"
router = routers.DefaultRouter()
router.register(r"scan", views.ScanViewSet)
router.register(r"nifti", views.NiftiViewSet)
router.register(r"sequence_type", views.SequenceTypeViewSet)
router.register(r"sequence_type_definition", views.SequenceTypeDefinitionViewSet)


urlpatterns = [
    path("mri/", include(router.urls)),
    path(
        "mri/scan/from_file/",
        views.ScanViewSet.as_view({"post": "from_file"}),
        name="from_file",
    ),
    path(
        "mri/scan/from_dicom/<int:series_id>/",
        views.ScanViewSet.as_view({"get": "from_dicom"}),
        name="from_dicom",
    ),
    path(
        "mri/scan/plot/<int:scan_id>/",
        views.ScanViewSet.as_view({"get": "plot"}),
        name="plot",
    ),
]
