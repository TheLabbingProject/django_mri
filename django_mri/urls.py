from django.urls import path, include
from django_mri import views
from django_mri.tests.views import Fake_group, Fake_study, Fake_subject
from rest_framework import routers
from django.conf import settings

app_name = "mri"
router = routers.DefaultRouter()
router.register(r"scan", views.ScanViewSet)
router.register(r"nifti", views.NiftiViewSet)
router.register(r"sequence_type", views.SequenceTypeViewSet)

if getattr(settings, "TEST", False):
    app_name = "tests"
    test_router = routers.DefaultRouter()
    router.register(r"group", Fake_group.GroupViewSet)
    router.register(r"subject", Fake_subject.SubjectViewSet)
    router.register(r"study", Fake_study.StudyViewSet)


urlpatterns = [
    path("mri/", include(router.urls)),
    path("mri/scan/from_file/", views.ScanViewSet.as_view({"POST": "from_file"})),
    path(
        "mri/scan/from_dicom/<int:series_id>/",
        views.ScanViewSet.as_view({"GET": "from_dicom"}),
    ),
    path("mri/scan/plot/<int:scan_id>/", views.ScanViewSet.as_view({"get": "plot"})),
]

if getattr(settings, "TEST", False):
    urlpatterns.append(path("tests/", include(test_router)))
