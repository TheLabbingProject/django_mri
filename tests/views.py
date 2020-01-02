from tests.models import Subject, Group
from rest_framework import viewsets
from django_mri.views.defaults import DefaultsMixin


class SubjectViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.subject.Subject` instances
    to be viewed or edited.

    """

    queryset = Subject.objects.order_by("-id").all()

    def get_queryset(self):
        # TODO: Implement filtering according to the user's collaborations
        return Subject.objects.all()


class GroupViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows :class:`~research.models.group.Group` instances
    to be viewed or edited.
    
    """

    queryset = Group.objects.order_by("id").all()
