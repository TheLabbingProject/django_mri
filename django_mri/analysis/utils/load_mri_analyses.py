"""
Definition of the
:func:`~django_mri.analysis.utils.load_mri_analyses.load_mri_analyses`
function.
"""

from django_analyses.models.analysis import Analysis
from django_analyses.models.pipeline import Pipeline
from django_mri.analysis.analysis_definitions import analysis_definitions
from django_mri.analysis.pipeline_definitions import pipeline_definitions


def load_mri_analyses():
    """
    Imports the app's preconfigured MRI analyses and pipelines to the database.
    """

    Analysis.objects.from_list(analysis_definitions)
    Pipeline.objects.from_list(pipeline_definitions)
