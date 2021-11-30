"""
The app's URLs configuration.

References
----------
* `URL dispatcher`_

.. _URL dispatcher:
   https://docs.djangoproject.com/en/3.0/topics/http/urls/#url-dispatcher
"""
from django.urls import include, path
from rest_framework import routers

from django_mri import views

app_name = "mri"

#: Automatic URL routing using Django REST Framework.
#:
#: References
#: ----------
#: * Routers_
#:
#: .. _Routers:
#:    https://www.django-rest-framework.org/api-guide/routers/
router = routers.DefaultRouter()
router.register(r"scan", views.ScanViewSet)
router.register(r"nifti", views.NiftiViewSet)
router.register(r"session", views.SessionViewSet)
router.register(r"irb_approval", views.IrbApprovalViewSet)


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
    path(
        "mri/scan/<int:scan_id>/runs/",
        views.ScanViewSet.as_view({"get": "query_scan_run_set"}),
        name="query_scan_run_set",
    ),
    path(
        "mri/scan/nifti_zip/<str:scan_ids>/",
        views.ScanViewSet.as_view({"get": "listed_nifti_zip"}),
        name="listed_nifti_zip",
    ),
    path(
        "mri/scan/to_zip/<str:file_formats>/<str:scan_ids>/",
        views.ScanViewSet.as_view({"get": "to_zip"}),
        name="to_zip",
    ),
    path(
        "mri/scan/<int:scan_id>/nilearn_plot/",
        views.ScanViewSet.as_view({"get": "nilearn_plot"}),
        name="nilearn_plot",
    ),
    path(
        "mri/scan/<int:scan_id>/nifti_zip/",
        views.ScanViewSet.as_view({"get": "nifti_zip"}),
        name="nifti_zip",
    ),
    path(
        "mri/nifti/<int:nifti_id>/to_zip/",
        views.NiftiViewSet.as_view({"get": "to_zip"}),
        name="nifti_to_zip",
    ),
    path(
        "mri/session/<int:session_id>/dicom_zip/",
        views.SessionViewSet.as_view({"get": "dicom_zip"}),
        name="session_dicom_zip",
    ),
    path(
        "mri/session/<int:session_id>/nifti_zip/",
        views.SessionViewSet.as_view({"get": "nifti_zip"}),
        name="session_nifti_zip",
    ),
]
