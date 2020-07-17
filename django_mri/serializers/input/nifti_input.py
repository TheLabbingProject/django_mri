"""
Definition of the
:class:`~django_mri.serializers.input.nifti_input.NiftiInputSerializer`
class.
"""

from django_mri.models.inputs.nifti_input import NiftiInput
from django_mri.models.nifti import NIfTI
from rest_framework import serializers


class NiftiInputSerializer(serializers.ModelSerializer):
    """
    Serializer for the
    :class:`~django_mri.models.inputs.nifti_input.NiftiInput`
    model.
    """

    #: Hyperlink to the actual :class:`django_mri.models.nifti.NIfTI` instance
    #: that was used.
    value = serializers.HyperlinkedRelatedField(
        view_name="mri:nifti-detail", queryset=NIfTI.objects.all()
    )

    class Meta:
        model = NiftiInput
        fields = "id", "key", "value", "run", "definition"
