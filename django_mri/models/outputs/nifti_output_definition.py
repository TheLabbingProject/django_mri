from pathlib import Path

from django_analyses.models.output.definitions.output_definition import \
    OutputDefinition

from django_mri.models.nifti import NIfTI
from django_mri.models.outputs.nifti_output import NiftiOutput


class NiftiOutputDefinition(OutputDefinition):
    output_class = NiftiOutput

    def pre_output_instance_create(self, kwargs: dict) -> None:
        value = kwargs.get("value")
        is_path = isinstance(value, (str, Path))
        if is_path:
            kwargs["value"] = NIfTI.objects.create(path=str(value), is_raw=False)
        super().pre_output_instance_create(kwargs)
