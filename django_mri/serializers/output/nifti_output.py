from django_mri.models.nifti import NIfTI
from django_mri.models.outputs.nifti_output import NiftiOutput
from rest_framework import serializers


class NiftiOutputSerializer(serializers.ModelSerializer):
    value = serializers.HyperlinkedRelatedField(
        view_name="mri:nifti-detail", queryset=NIfTI.objects.all()
    )

    class Meta:
        model = NiftiOutput
        fields = "id", "key", "value", "run", "definition"
