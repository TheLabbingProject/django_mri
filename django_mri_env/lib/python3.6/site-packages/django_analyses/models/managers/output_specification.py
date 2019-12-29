from django.db import models
from django.db.models import Count, QuerySet
from django_analyses.models.output.definitions.output_definition import OutputDefinition


class OutputSpecificationManager(models.Manager):
    def filter_by_definitions(self, analysis, definitions: list) -> QuerySet:
        possibly_same = self.filter(
            analysis=analysis, base_output_definitions__in=definitions
        )
        return possibly_same.annotate(
            base_output_definitions__count=Count("base_output_definitions")
        ).filter(base_output_definitions__count=len(definitions))

    def from_dict(self, analysis, specification: dict) -> tuple:
        output_definitions = OutputDefinition.objects.from_specification_dict(
            specification
        )
        existing_specification = self.filter_by_definitions(
            analysis, output_definitions
        )
        if not existing_specification:
            new_specification = self.create(analysis=analysis)
            new_specification.base_output_definitions.set(output_definitions)
            return new_specification, True
        return existing_specification[0], False
