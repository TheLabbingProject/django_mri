from django.urls import path, include
from django_mri import views
from rest_framework import routers

app_name = "mri"
router = routers.DefaultRouter()
router.register(r"scan", views.ScanViewSet)
router.register(r"tree/unreviewed_dicom_patients", views.UnreviewedDicomPatientViewSet)
router.register(r"tree/unreviewed_dicom_series", views.UnreviewedDicomSeriesViewSet)


mripatterns = (
    [
        path("scan/create/", views.CreateScanView.as_view(), name="scan_create"),
        path(
            "scan/create/from_dicom/<int:pk>/",
            views.CreateScanFromDicom.as_view(),
            name="scan_create_from_dcm",
        ),
    ],
    app_name,
)

urlpatterns = [
    path("", include(mripatterns)),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
