from django.db import models
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.output.output_specification import OutputSpecification


class AnalysisVersionManager(models.Manager):
    def from_dict(self, analysis, definition: dict):
        input_specification, created_input_spec = InputSpecification.objects.from_dict(
            analysis, definition["input"]
        )
        (
            output_specification,
            created_output_spec,
        ) = OutputSpecification.objects.from_dict(analysis, definition["output"])
        return self.get_or_create(
            analysis=analysis,
            title=definition.get("title", "1.0.0"),
            description=definition.get("description"),
            input_specification=input_specification,
            output_specification=output_specification,
            nested_results_attribute=definition.get("nested_results_attribute"),
        )

    def from_list(self, analysis, definitions: list) -> dict:
        results = {}
        for version_definition in definitions:
            version, created = self.from_dict(analysis, version_definition)
            results[version.title] = {"model": version, "created": created}
        return results
