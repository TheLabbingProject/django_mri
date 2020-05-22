from django_mri.models import NIfTI
from rest_framework import serializers


class NiftiSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mri:nifti-detail")

    class Meta:
        model = NIfTI
        exclude = ("path",)
