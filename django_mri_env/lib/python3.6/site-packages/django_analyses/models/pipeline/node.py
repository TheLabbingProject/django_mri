from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel


class Node(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )
    configuration = JSONField()

    class Meta:
        ordering = ("-created",)

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)

    def validate(self) -> None:
        self.analysis_version.input_specification.validate_keys(**self.configuration)

    def run(self, inputs: dict) -> Run:
        run_configuration = self.configuration.copy()
        run_configuration.update(inputs)
        return Run.objects.get_or_execute(self.analysis_version, **run_configuration)

    def get_required_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_destination_set.values_list("source", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def get_requiring_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_source_set.values_list("destination", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def check_configuration_sameness(self, key: str, value) -> bool:
        input_definition = self.analysis_version.get_input_definition(key=key)
        is_same = value == self.configuration.get(key)
        is_default = (
            value == input_definition.default and self.configuration.get(key) is None
        )
        not_configuration = input_definition.is_configuration is False
        return is_same or is_default or not_configuration

    def check_run_configuration_sameness(self, run: Run) -> bool:
        return all(
            [
                self.check_configuration_sameness(key, value)
                for key, value in run.input_configuration.items()
            ]
        )

    def get_run_set(self) -> models.QuerySet:
        all_runs = Run.objects.filter(analysis_version=self.analysis_version)
        return [run for run in all_runs if self.check_run_configuration_sameness(run)]

    @property
    def required_nodes(self) -> models.QuerySet:
        return self.get_required_nodes() or None

    @property
    def requiring_nodes(self) -> models.QuerySet:
        return self.get_requiring_nodes() or None

    @property
    def run_set(self) -> models.QuerySet:
        return self.get_run_set()
