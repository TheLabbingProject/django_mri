from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


class DefaultsMixin:
    """
    Default settings for view authentication, permissions and filtering.
    
    """

    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
