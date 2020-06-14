from django.test import TestCase
from django_dicom.models import Image
from django_analyses.models import AnalysisVersion, Run
from django_mri.models import Scan, NIfTI
from django_mri.models.inputs import NiftiInput, NiftiInputDefinition
from tests.models import Subject
from tests.fixtures import (
    SIEMENS_DWI_SERIES,
    SIEMENS_DWI_SERIES_PATH,
)

from pathlib import Path
from django.db.models import signals
import factory
from django_mri.serializers.input import NiftiInputSerializer
from django_mri.serializers.input.nifti_input_definition import (
    NiftiInputDefinitionSerializer,
)
from django_mri import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


class NiftiInputModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        subject = Subject.objects.create()
        Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
        scan = Scan.objects.create(dicom=Image.objects.first().series, subject=subject)
        nifti = scan.nifti
        definition = NiftiInputDefinition.objects.create(key="test")
        version = AnalysisVersion.objects.create(
            title="TestVersion", description="desc"
        )
        run = Run.objects.create(analysis_version=version)
        NiftiInput.objects.create(value=nifti, definition=definition, run=run)

    def setUp(self):
        self.nifti = NIfTI.objects.last()
        self.input = NiftiInput.objects.last()
        self.definition = NiftiInputDefinition.objects.last()
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.nifti_serializer = serializers.NiftiSerializer(
            instance=self.nifti, context={"request": req}
        )
        self.input_serializer = NiftiInputSerializer(
            instance=self.input, context={"request": req}
        )

    def test_serializer(self):
        expected = {
            "id": self.input.id,
            "key": self.definition.key,
            "value": self.nifti_serializer.data["url"],
            "run": Run.objects.last().id,
            "definition": self.definition.id,
        }
        result = self.input_serializer.data
        self.assertDictEqual(result, expected)


class NiftiInputDefinitionModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        definition = NiftiInputDefinition.objects.create(key="test")

    def setUp(self):
        self.definition = NiftiInputDefinition.objects.last()
        fact = APIRequestFactory()
        request = fact.get("/")
        req = Request(request)
        self.definition_serializer = NiftiInputDefinitionSerializer(
            instance=self.definition, context={"request": req}
        )

    def test_definition_serializer(self):
        expected = {
            "id": self.definition.id,
            "key": self.definition.key,
            "required": self.definition.required,
            "description": self.definition.description,
            "is_configuration": self.definition.is_configuration,
            "value_attribute": self.definition.value_attribute,
            "run_method_input": self.definition.run_method_input,
        }
        result = self.definition_serializer.data
        self.assertDictEqual(result, expected)
