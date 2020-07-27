"""
The app's URLs configuration.

References
----------
* `URL dispatcher`_

.. _URL dispatcher:
   https://docs.djangoproject.com/en/3.0/topics/http/urls/#url-dispatcher
"""

from django.urls import path, include
from django_mri import views
from rest_framework import routers

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
