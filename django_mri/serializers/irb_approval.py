"""
Definition of the :class:`IrbApprovalSerializer` class.
"""
from django_mri.models.irb_approval import IrbApproval
from rest_framework import serializers


class IrbApprovalSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for the
    :class:`~django_mri.models.irb_approval.IrbApproval` model.

    References
    ----------
    * https://www.django-rest-framework.org/api-guide/serializers/
    """

    class Meta:
        model = IrbApproval
        fields = "id", "institution", "number"
