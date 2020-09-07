from bokeh.client import pull_session
from bokeh.embed import server_session
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django_dicom.models import Series
from django_mri.filters.scan_filter import ScanFilter
from django_mri.models.session import Session
from django_mri.serializers import SessionSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.views.utils import fix_bokeh_script
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.conf import settings


class SessionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Session.objects.order_by("-time__date", "time__time")
    serializer_class = SessionSerializer
    ordering_fields = ("url", "subject", "comments", "time", "scan_set")

    # def get_queryset(self) -> QuerySet:
    #     """
    #     Filter the returned scans according to the studies the requesting
    #     user is a collaborator in, unless the user is staff, in which case
    #     return all scans.

    #     Returns
    #     -------
    #     QuerySet
    #         Scan instances.
    #     """

    #     user = get_user_model().objects.get(username=self.request.user)
    #     queryset = super().get_queryset()
    #     if user.is_staff:
    #         return queryset
    #     return queryset.filter(study_groups__study__collaborators=user)
