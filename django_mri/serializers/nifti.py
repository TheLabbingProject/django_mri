from django_mri.models import Scan, NIfTI
from rest_framework import serializers


class NiftiSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mri:nifti-detail")
    parent = serializers.HyperlinkedRelatedField(
        view_name="mri:scan-detail", queryset=Scan.objects.all()
    )

    class Meta:
        model = NIfTI
        exclude = ("path",)
