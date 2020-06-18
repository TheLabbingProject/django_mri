from django.test import TestCase
from django_dicom.models import Image
from django_analyses.models import AnalysisVersion, Run
from django_mri.models import Scan, NIfTI
from django_mri.models.outputs import NiftiOutput, NiftiOutputDefinition
from django_mri.models.outputs.output_definitions import OutputDefinitions
from tests.models import Subject
from tests.fixtures import (
    NIFTI_TEST_FILE_PATH,
    SIEMENS_DWI_SERIES,
    SIEMENS_DWI_SERIES_PATH,
)

from pathlib import Path
from django.db.models import signals
import factory
from django_mri.serializers.output import NiftiOutputSerializer
from django_mri.serializers.output.nifti_output_definition import (
    NiftiOutputDefinitionSerializer,
)
from django_mri import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


class NiftiOutputModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        subject = Subject.objects.create()
        Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
        scan = Scan.objects.create(dicom=Image.objects.first().series, subject=subject)
        nifti = scan.nifti
        definition = NiftiOutputDefinition.objects.create(key="test")
        version = AnalysisVersion.objects.create(
            title="TestVersion", description="desc"
        )
        run = Run.objects.create(analysis_version=version)
        NiftiOutput.objects.create(value=nifti, definition=definition, run=run)

    def setUp(self):
        self.nifti = NIfTI.objects.last()
        self.output = NiftiOutput.objects.last()
        self.definition = NiftiOutputDefinition.objects.last()
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.nifti_serializer = serializers.NiftiSerializer(
            instance=self.nifti, context={"request": req}
        )
        self.output_serializer = NiftiOutputSerializer(
            instance=self.output, context={"request": req}
        )

    def test_serializer(self):
        expected = {
            "id": self.output.id,
            "key": self.definition.key,
            "value": self.nifti_serializer.data["url"],
            "run": Run.objects.last().id,
            "definition": self.definition.id,
        }
        result = self.output_serializer.data
        self.assertDictEqual(result, expected)


class NiftiOutputDefinitionModelTestCase(TestCase):
    def setUp(self):
        self.definition = NiftiOutputDefinition.objects.create(key="test")
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.definition_serializer = NiftiOutputDefinitionSerializer(
            instance=self.definition, context={"request": req}
        )

    def test_serializer(self):
        expected = {
            "id": self.definition.id,
            "key": self.definition.key,
            "description": self.definition.description,
        }
        result = self.definition_serializer.data
        self.assertDictEqual(result, expected)

    def test_pre_output_instance_create(self):
        self.definition.pre_output_instance_create(
            kwargs={"value": NIFTI_TEST_FILE_PATH}
        )
        result = NIfTI.objects.last()
        self.assertIsNotNone(result)

    def test_pre_output_instance_create_without_path(self):
        self.definition.pre_output_instance_create(kwargs={})
        result = NIfTI.objects.last()
        self.assertIsNone(result)


class OutputDefinitionsEnumTestCase(TestCase):
    def test_scan_value(self):
        expected = ["Scan", "NIfTI"]
        result = []
        for selection in OutputDefinitions:
            result.append(selection.value)
        self.assertListEqual(result, expected)
