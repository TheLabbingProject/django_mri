import factory

from django.db.models import signals
from django.test import TestCase
from django_analyses.models import (
    Analysis,
    Pipeline,
)
from django_dicom.models import Image
from django_mri.models import Scan, NIfTI
from django_mri.analysis.analysis_definitions import analysis_definitions
from pathlib import Path
from tests.factories import SubjectFactory
from tests.fixtures import SIEMENS_DWI_SERIES_PATH


class AnalysisModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        subject = SubjectFactory()
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        cls.scan = Scan.objects.create(
            dicom=Image.objects.first().series, subject=subject
        )
        cls.analyses = Analysis.objects.from_list(analysis_definitions)

    def test_analyses_creation(self):
        self.assertIsNotNone(self.analyses)
        self.assertIsInstance(self.analyses, dict)

    def test_pipline_creation(self):
        nifti_path = Path("MNI152_T1_2mm_brain/1.nii.gz")
        NIfTI.objects.create(path=nifti_path)
        from django_mri.analysis.pipeline_definitions import (
            pipeline_definitions,
        )

        pipelines = Pipeline.objects.from_list(pipeline_definitions)
        self.assertIsNotNone(pipelines)
        self.assertIsInstance(pipelines, list)
