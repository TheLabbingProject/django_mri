from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from django_analyses.models.input.input import Input
from django_analyses.models.managers.run import RunManager
from django_analyses.models.output.output import Output
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.SET_NULL,
    )

    objects = RunManager()

    class Meta:
        ordering = ("-created",)

    def get_input_configuration(self) -> dict:
        configuration = {
            inpt.definition.key: inpt.value
            for inpt in self.input_set.select_subclasses()
        }
        defaults = self.input_defaults.copy()
        defaults.update(configuration)
        return defaults

    def get_output_configuration(self) -> dict:
        return {output.key: output.value for output in self.output_set}

    def create_input_instance(self, key: str, value) -> Input:
        input_definition = self.analysis_version.input_definitions.get(key=key)
        return input_definition.create_input_instance(value=value, run=self)

    def get_missing_output_path_definitions(self, **kwargs) -> list:
        return [
            definition
            for definition in self.analysis_version.input_definitions
            if isinstance(definition, StringInputDefinition)
            and definition.is_output_path
            and definition.key not in kwargs
        ]

    def create_missing_output_path_definitions(self, **kwargs) -> list:
        return [
            output_path_definition.create_input_instance(run=self)
            for output_path_definition in self.get_missing_output_path_definitions(
                **kwargs
            )
        ]

    def create_input_instances(self, **kwargs) -> list:
        input_instances = [
            self.create_input_instance(key, value) for key, value in kwargs.items()
        ]
        input_instances += self.create_missing_output_path_definitions(**kwargs)
        return input_instances

    def create_output_instance(self, key: str, value) -> Output:
        output_definition = self.analysis_version.output_definitions.get(key=key)
        return output_definition.create_output_instance(value=value, run=self)

    def create_output_instances(self, **results) -> list:
        return [
            self.create_output_instance(key, value) for key, value in results.items()
        ]

    def get_input_set(self) -> models.QuerySet:
        return self.base_input_set.select_subclasses()

    def get_output_set(self) -> models.QuerySet:
        return self.base_output_set.select_subclasses()

    @property
    def input_defaults(self) -> dict:
        return self.analysis_version.input_specification.default_configuration

    @property
    def input_configuration(self) -> dict:
        return self.get_input_configuration()

    @property
    def output_configuration(self) -> dict:
        return self.get_output_configuration()

    @property
    def input_set(self) -> models.QuerySet:
        return self.get_input_set()

    @property
    def output_set(self) -> models.QuerySet:
        return self.get_output_set()
