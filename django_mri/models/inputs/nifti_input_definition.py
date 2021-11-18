from django_analyses.models.input.definitions.input_definition import \
    InputDefinition

from django_mri.models.inputs.nifti_input import NiftiInput


class NiftiInputDefinition(InputDefinition):
    input_class = NiftiInput
