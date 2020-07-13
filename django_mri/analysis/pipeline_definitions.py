"""
Aggregates pipeline definitions from :mod:`django_mri.analysis.pipelines`.
The created list (*pipeline_definitions*) may easily be imported to the
database using the
:meth:`~django_analysis.models.managers.pipline.PipelineManager.from_list`
method.
"""

from django_mri.analysis.pipelines.basic_fsl_preprocessing import (
    BASIC_FSL_PREPROCESSING,
)
from django_mri.analysis.pipelines.fieldmap_correction import (
    FIELDMAP_CORRECTION,
)

pipeline_definitions = [BASIC_FSL_PREPROCESSING, FIELDMAP_CORRECTION]
