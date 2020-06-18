from django.test import TestCase
from django_dicom.models import Image
from django_analyses.models import (
    AnalysisVersion,
    Run,
    Analysis,
    InputSpecification,
    OutputSpecification,
    Pipeline,
)
from django_mri.models import Scan, NIfTI
from django_mri.analysis.analysis_definitions import analysis_definitions
from tests.models import Subject
from tests.fixtures import (
    SIEMENS_DWI_SERIES,
    SIEMENS_DWI_SERIES_PATH,
)

from pathlib import Path
from django.db.models import signals
import factory


class AnalysisModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        subject = Subject.objects.create()
        Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
        scan = Scan.objects.create(dicom=Image.objects.first().series, subject=subject)

    def setUp(self):
        self.scan = Scan.objects.last()
        self.analyses = Analysis.objects.from_list(analysis_definitions)

    def test_analyses_creation(self):
        self.assertIsNotNone(self.analyses)
        self.assertIsInstance(self.analyses, dict)

    def test_pipline_creation(self):
        nifti_path = Path("MNI152_T1_2mm_brain/1.nii.gz")
        NIfTI.objects.create(path=nifti_path)
        from django_mri.analysis.pipeline_definitions import pipeline_definitions

        pipelines = Pipeline.objects.from_list(pipeline_definitions)
        self.assertIsNotNone(pipelines)
        self.assertIsInstance(pipelines, list)
