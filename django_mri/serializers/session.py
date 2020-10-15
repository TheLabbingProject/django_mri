"""
Definition of the :class:`~django_mri.serializers.session.SessionSerializer` class.
"""

from django_mri.serializers.scan import ScanSerializer
from django_mri.models.session import Session
from django_mri.utils.utils import get_subject_model, get_group_model
from rest_framework import serializers


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the :class:`~django_mri.models.session.Session` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    url = serializers.HyperlinkedIdentityField(view_name="mri:session-detail")
    subject = serializers.HyperlinkedRelatedField(
        view_name="research:subject-detail", queryset=get_subject_model().objects.all(),
    )
    scan_set = ScanSerializer(many=True)

    class Meta:
        model = Session
        fields = ("id", "url", "subject", "comments", "time", "scan_set")
