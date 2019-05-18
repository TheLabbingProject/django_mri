from django.apps import apps
from django.conf import settings
from django_dicom.models import Series
from django_mri.models import Scan, NIfTI
from django_mri.models.sequence_type import SequenceType
from rest_framework import serializers

subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)


class SequenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SequenceType
        fields = "__all__"


class NiftiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NIfTI
        fields = "__all__"


class ScanSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mri:scan-detail")
    # dicom = serializers.HyperlinkedRelatedField(
    #     view_name="dicom:series-detail", queryset=Series.objects.all()
    # )
    # subject = serializers.HyperlinkedRelatedField(
    #     view_name="research:subject-detail", queryset=Subject.objects.all()
    # )

    class Meta:
        model = Scan
        exclude = ("subject", "_nifti", "sequence_type", "dicom")

