from django.db import models
from django_analyses.models.analysis_version import AnalysisVersion


class RunManager(models.Manager):
    def get_existing(self, analysis_version: AnalysisVersion, **kwargs):
        runs = self.filter(analysis_version=analysis_version)
        configuration = analysis_version.update_input_with_defaults(**kwargs)
        matching = [run for run in runs if run.input_configuration == configuration]
        return matching[0] if matching else None

    def create_and_execute(self, analysis_version: AnalysisVersion, **kwargs):
        run = self.create(analysis_version=analysis_version)
        inputs_instances = run.create_input_instances(**kwargs)
        updated_kwargs = {inpt.key: inpt.value for inpt in inputs_instances}
        results = analysis_version.run(**updated_kwargs)
        run.create_output_instances(**results)
        return run

    def get_or_execute(self, analysis_version: AnalysisVersion, **kwargs):
        existing = self.get_existing(analysis_version, **kwargs)
        return existing or self.create_and_execute(analysis_version, **kwargs)

