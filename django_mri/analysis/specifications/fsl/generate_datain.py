"""
Input and output specification dictionaries for FSL's fslroi_ script.

.. _fslroi:
   https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fslroi
"""
from django_mri.models.inputs.nifti_input_definition import (
    NiftiInputDefinition,
)
from django_analyses.models.output.definitions import FileOutputDefinition

#: *fslroi* input specification dictionary.
GENERATE_DATAIN_INPUT_SPECIFICATION = {
    "in_file": {
        "type": NiftiInputDefinition,
        "required": True,
        "description": "A NIfTI to generate datain.txt file according to.",
        "is_configuration": False,
        "value_attribute": "path.__str__",
    },

#: *generate_datain* output specification dictionary.
GENERATE_DATAIN_OUTPUT_SPECIFICATION = {
    "datain_file": {
        "type": FileOutputDefinition,
        "description": "Path to output file.",
    },
}
