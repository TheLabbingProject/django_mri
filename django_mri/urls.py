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
router.register(r"sequence_type", views.SequenceTypeViewSet)
router.register(
    r"sequence_type_definition", views.SequenceTypeDefinitionViewSet
)
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
        "mri/scan/<int:scan_id>/nilearn_plot/",
        views.ScanViewSet.as_view({"get": "nilearn_plot"}),
        name="nilearn_plot",
    ),
]
