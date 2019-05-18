from django.apps import apps
from django.conf import settings
from django_dicom.models import Series, Patient
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
    dicom = serializers.HyperlinkedRelatedField(
        view_name="dicom:series-detail", queryset=Series.objects.all()
    )
    # subject = serializers.HyperlinkedRelatedField(
    #     view_name="research:subject-detail", queryset=Subject.objects.all()
    # )

    class Meta:
        model = Scan
        exclude = ("subject", "_nifti", "sequence_type")


class DicomPatientToTreeNode(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ("id", "name", "children", "file")

    def get_id(self, patient):
        return f"dicom_patient_{patient.id}"

    def get_name(self, patient):
        return patient.get_full_name()

    def get_children(self, patient):
        return []

    def get_file(self, patient):
        return "subject"


class DicomSeriesToTreeNode(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField(source="description")
    file = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ("id", "name", "file")

    def get_id(self, series):
        return f"dicom_series_{series.id}"

    def get_file(self, series):
        return "dcm"

