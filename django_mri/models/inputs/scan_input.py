from django.db import models
from django_analyses.models.input.input import Input


class ScanInput(Input):
    value = models.ForeignKey(
        "django_mri.Scan", on_delete=models.PROTECT, related_name="run_input_set"
    )
    definition = models.ForeignKey(
        "django_mri.ScanInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )
