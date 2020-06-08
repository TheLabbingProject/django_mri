from django.urls import path, include
from rest_framework import routers
from .views import SubjectViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r"subject", SubjectViewSet)
router.register(r"group", GroupViewSet)

urlpatterns = [
    path("", include("django_dicom.urls")),
    path("", include("django_mri.urls")),
    path("", include((router.urls, "research"), namespace="research")),
]
