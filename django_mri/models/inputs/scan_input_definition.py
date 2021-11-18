from django_analyses.models.input.definitions.input_definition import \
    InputDefinition

from django_mri.models.inputs.scan_input import ScanInput


class ScanInputDefinition(InputDefinition):
    input_class = ScanInput
