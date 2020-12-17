from django_mri.models.irb_approval import IrbApproval
from django_mri.serializers.irb_approval import IrbApprovalSerializer
from django_mri.views.defaults import DefaultsMixin
from django_mri.views.pagination import StandardResultsSetPagination
from django_mri.filters.irb_approval_filter import IrbApprovalFilter
from rest_framework import viewsets


class IrbApprovalViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed or edited.
    """

    pagination_class = StandardResultsSetPagination
    queryset = IrbApproval.objects.order_by("institution", "number")
    serializer_class = IrbApprovalSerializer
    filter_class = IrbApprovalFilter
    search_fields = "id", "institution", "number"
    ordering_fields = "id", "institution", "number"
