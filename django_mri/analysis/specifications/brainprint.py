"""
Input and output specification dictionaries for the Brainprint interface.
"""
from django.conf import settings
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import ListOutputDefinition
from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)

#: *Brainprint* input specification.
BRAINPRINT_INPUT_SPECIFICATION = {
    "subjects_dir": {
        "type": DirectoryInputDefinition,
        "default": settings.ANALYSIS_BASE_PATH,
        "required": True,
        "description": "Path to subjects directory.",
        "is_configuration": False,
    },
    "subject_id": {
        "type": StringInputDefinition,
        "description": "Directory name within *subjects_dir* in which FreeSurfer results can be found.",
        "required": True,
        "is_configuration": False,
        "run_method_input": True,
    },
    "num": {
        "type": IntegerInputDefinition,
        "description": "Number of eigenvalues to compute, by default 50.",
        "default": 50,
    },
    "skip_cortex": {
        "type": BooleanInputDefinition,
        "description": "",
        "default": False,
    },
    "reweight": {
        "type": BooleanInputDefinition,
        "description": "Whether to reweight eigenvalues or not, by default False.",
        "default": False,
    },
    "keep_eigenvectors": {
        "type": BooleanInputDefinition,
        "description": "Whether to also return eigenvectors or not, by default False.",
        "default": False,
    },
    "keep_temp": {
        "type": BooleanInputDefinition,
        "description": "Whether to keep the temporary files directory or not, by default False.",
        "default": False,
    },
    "asymmetry": {
        "type": BooleanInputDefinition,
        "description": "Whether to calculate asymmetry between lateral structures, by default False.",
        "default": False,
    },
    "destination": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "required": True,
        "description": "The directory where the output files should be stored. If you are running group level analysis this folder should be prepopulated with the results of the participant level analysis.",
        "is_configuration": False,
        "run_method_input": True,
    },
    "norm": {
        "type": StringInputDefinition,
        "choices": ["surface", "volume", "geometry", "none"],
        "default": "none",
        "description": "Eigenvalues normalization method, by default 'none'.",
    },
    "asymmetry_distance": {
        "type": StringInputDefinition,
        "choices": ["euc"],
        "default": "euc",
        "description": "Distance measurement to use if *asymmetry* is set to True, by default 'euc'.",
    },
}
#: *Brainprint* output specification.
BRAINPRINT_OUTPUT_SPECIFICATION = {
    "eigenvalues": {
        "type": FileOutputDefinition,
        "description": "Eigenvalues CSV.",
    },
    "eigenvectors": {
        "type": FileOutputDefinition,
        "description": "Eigenvectors CSV.",
    },
    "distances": {
        "type": FileOutputDefinition,
        "description": "Lateral distances CSV.",
    },
}


# flake8: noqa: E501
