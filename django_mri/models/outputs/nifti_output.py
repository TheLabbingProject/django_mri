from django.db import models
from django_analyses.models.output.output import Output
from django_mri.models.nifti import NIfTI
from pathlib import Path


class NiftiOutput(Output):
    value = models.ForeignKey(
        "django_mri.NIfTI", on_delete=models.PROTECT, related_name="run_output_set"
    )
    definition = models.ForeignKey(
        "django_mri.NiftiOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )
