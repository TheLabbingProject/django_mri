from django.db import models
from django_analyses.models.managers.output_specification import (
    OutputSpecificationManager,
)
from django_extensions.db.models import TimeStampedModel


class OutputSpecification(TimeStampedModel):
    analysis = models.ForeignKey("django_analyses.Analysis", on_delete=models.CASCADE)
    base_output_definitions = models.ManyToManyField("django_analyses.OutputDefinition")

    objects = OutputSpecificationManager()

    def __str__(self) -> str:
        definitions = self.output_definitions.select_subclasses()
        formatted_definitions = "\n\t".join(
            [str(definition) for definition in definitions]
        )
        return f"\n[{self.analysis}]\n\t{formatted_definitions}\n"

    @property
    def output_definitions(self) -> models.QuerySet:
        return self.base_output_definitions.select_subclasses()
