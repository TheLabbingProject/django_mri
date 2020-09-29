from django.db import models
from django_analyses.models.input.input import Input


class NiftiInput(Input):
    value = models.ForeignKey(
        "django_mri.NIfTI", on_delete=models.PROTECT, related_name="run_input_set",
    )
    definition = models.ForeignKey(
        "django_mri.NiftiInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )
