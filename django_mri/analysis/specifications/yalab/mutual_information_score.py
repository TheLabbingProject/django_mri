from django_analyses.models.input.definitions import (
    FileInputDefinition,
    IntegerInputDefinition,
)
from django_analyses.models.output.definitions import FloatOutputDefinition

MUTUAL_INFORMATION_SCORE_INPUT_SPECIFICATION = {
    "anatomical_1": {
        "type": FileInputDefinition,
        "required": True,
        "description": "First anatomical.",
        "is_configuration": False,
        "run_method_input": True,
    },
    "anatomical_2": {
        "type": FileInputDefinition,
        "required": True,
        "description": "Second anatomical.",
        "is_configuration": False,
        "run_method_input": True,
    },
    "bins": {
        "type": IntegerInputDefinition,
        "description": "Number of bins used in the transformation to a 2D histogram.",  # noqa: E501
        "required": False,
        "default": 10,
        "is_configuration": True,
    },
}

MUTUAL_INFORMATION_SCORE_OUTPUT_SPECIFICATION = {
    "score": {
        "type": FloatOutputDefinition,
        "description": "Mutual information score.",
    }
}
