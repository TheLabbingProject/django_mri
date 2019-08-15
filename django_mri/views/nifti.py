from django_mri.models import NIfTI
from django_mri.serializers import NiftiSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class NiftiViewSet(DefaultsMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = NIfTI.objects.all()
    serializer_class = NiftiSerializer
