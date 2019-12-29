from django.db import models
from django_analyses.models.managers.output_definition import OutputDefinitionManager
from django_analyses.models.output.output import Output


class OutputDefinition(models.Model):
    key = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    objects = OutputDefinitionManager()

    OUTPUT_CLASS = None

    def __str__(self) -> str:
        return self.key

    def create_output_instance(self, **kwargs) -> Output:
        return self.OUTPUT_CLASS.objects.create(definition=self, **kwargs)
