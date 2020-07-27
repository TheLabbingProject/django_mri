from django.test import TestCase
from django_analyses.models import (
    Analysis,
    Pipeline,
)
from django_mri.analysis.analysis_definitions import analysis_definitions
from django_mri.models.nifti import NIfTI


CREATION_FAILURE_MESSAGE = (
    "Failed to create MRI {models} with the following exception:\n{exception}"
)
FAKE_MNI = "MNI152_T1_2mm_brain.nii.gz"


class AnalysesTestCase(TestCase):
    def test_analyses_creation(self):
        try:
            self.analyses = Analysis.objects.from_list(analysis_definitions)
        except Exception as e:
            message = CREATION_FAILURE_MESSAGE.format(
                models="analyses", exception=e
            )
            self.fail(message)
        else:
            self.assertIsInstance(self.analyses, dict)

    def test_pipline_creation(self):
        NIfTI.objects.create(path=FAKE_MNI)
        Analysis.objects.from_list(analysis_definitions)
        from django_mri.analysis.pipeline_definitions import pipeline_definitions
        
        try:
            pipelines = Pipeline.objects.from_list(pipeline_definitions)
        except Exception as e:
            message = CREATION_FAILURE_MESSAGE.format(
                models="pipelines", exception=e
            )
            self.fail(message)
        else:
            self.assertIsInstance(pipelines, list)
