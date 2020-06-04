from .models import Subject, Group
from rest_framework import viewsets
from django_mri.views.defaults import DefaultsMixin
from .serializers import SubjectSerializer


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~tests.models.Subject` instances
    to be viewed or edited.

    """

    queryset = Subject.objects.order_by("-id").all()
    serializer_class = SubjectSerializer


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~tests.models.Group` instances
    to be viewed or edited.
    
    """

    queryset = Group.objects.order_by("id").all()
