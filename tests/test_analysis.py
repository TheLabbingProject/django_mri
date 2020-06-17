from django.test import TestCase
from django_dicom.models import Image
from django_analyses.models import (
    AnalysisVersion,
    Run,
    Analysis,
    InputSpecification,
    OutputSpecification,
)
from django_mri.models import Scan
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
        # analyses = Analysis.objects.from_list(analysis_definitions)
        scan = Scan.objects.create(dicom=Image.objects.first().series, subject=subject)

    def setUp(self):
        self.scan = Scan.objects.last()

    # def test_recon_all(self):
    # result = self.scan.recon_all()
    # self.assertIsNotNone(result)
