from django_mri.filters.session_filter import SessionFilter
from django_mri.models.session import Session
from django_mri.serializers import (SessionReadSerializer,
                                    SessionWriteSerializer)
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.views.utils import ReadWriteSerializerMixin
from rest_framework import viewsets


class SessionViewSet(
    DefaultsMixin, ReadWriteSerializerMixin, viewsets.ModelViewSet
):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = Session.objects.order_by("-time__date", "-time__time")
    read_serializer_class = SessionReadSerializer
    write_serializer_class = SessionWriteSerializer
    filter_class = SessionFilter
    search_fields = ("id", "subject", "comments", "time", "scan_set")
    ordering_fields = (
        "id",
        "subject",
        "time__date",
        "time__time",
    )
