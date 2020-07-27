import factory

from django.db.models import signals
from django.test import TestCase
from django_analyses.models import AnalysisVersion, Run
from django_dicom.models import Image, Series
from django_mri import serializers
from django_mri.models import Scan
from django_mri.models.inputs import NiftiInput, NiftiInputDefinition
from django_mri.serializers.input import NiftiInputSerializer
from django_mri.serializers.input.nifti_input_definition import (
    NiftiInputDefinitionSerializer,
)
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from tests.factories import SubjectFactory
from tests.fixtures import SIEMENS_DWI_SERIES_PATH
from tests.utils import load_common_sequences


class NiftiInputModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        load_common_sequences()
        subject = SubjectFactory()
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        series = Series.objects.first()
        scan = Scan.objects.create(dicom=series, subject=subject)
        cls.nifti = scan.nifti
        cls.definition = NiftiInputDefinition.objects.create(key="test")
        version = AnalysisVersion.objects.create(
            title="TestVersion", description="desc"
        )
        run = Run.objects.create(analysis_version=version)
        cls.input = NiftiInput.objects.create(
            value=cls.nifti, definition=cls.definition, run=run
        )

    def setUp(self):
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
        cls.definition = NiftiInputDefinition.objects.create(key="test")

    def setUp(self):
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
            "db_value_preprocessing": self.definition.db_value_preprocessing,
            "run_method_input": self.definition.run_method_input,
            "db_value_preprocessing": self.definition.db_value_preprocessing,
        }
        result = self.definition_serializer.data
        self.assertDictEqual(result, expected)
