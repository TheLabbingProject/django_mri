from django_mri.models.inputs.scan_input import ScanInput
from django_mri.models.scan import Scan
from rest_framework import serializers


class ScanInputSerializer(serializers.ModelSerializer):
    value = serializers.HyperlinkedRelatedField(
        view_name="mri:scan-detail", queryset=Scan.objects.all()
    )

    class Meta:
        model = ScanInput
        fields = "id", "key", "value", "run", "definition"
