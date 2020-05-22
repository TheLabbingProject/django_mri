from django_mri.models.inputs.nifti_input import NiftiInput
from django_mri.models.nifti import NIfTI
from rest_framework import serializers


class NiftiInputSerializer(serializers.ModelSerializer):
    value = serializers.HyperlinkedRelatedField(
        view_name="mri:nifti-detail", queryset=NIfTI.objects.all()
    )

    class Meta:
        model = NiftiInput
        fields = "id", "key", "value", "run", "definition"
