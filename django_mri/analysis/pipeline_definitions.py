from django_mri.analysis.pipelines.basic_fsl_preprocessing import (
    BASIC_FSL_PREPROCESSING,
)
from django_mri.analysis.pipelines.fieldmap_correction import (
    FIELDMAP_CORRECTION,
)

pipeline_definitions = [BASIC_FSL_PREPROCESSING, FIELDMAP_CORRECTION]
