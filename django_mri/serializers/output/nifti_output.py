"""
Definition of the
:class:`~django_mri.serializers.output.nifti_output.NiftiOutputSerializer`
class.
"""

from django_mri.models.nifti import NIfTI
from django_mri.models.outputs.nifti_output import NiftiOutput
from rest_framework import serializers


class NiftiOutputSerializer(serializers.ModelSerializer):
    """
    Serializer for the
    :class:`~django_mri.models.outputs.nifti_output.NiftiOutput`
    model.
    """

    value = serializers.HyperlinkedRelatedField(
        view_name="mri:nifti-detail", queryset=NIfTI.objects.all()
    )

    class Meta:
        model = NiftiOutput
        fields = "id", "key", "value", "run", "definition"
