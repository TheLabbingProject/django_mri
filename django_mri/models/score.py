"""
Definition of the :class:`Score` model.
"""
import pandas as pd
from django.db import models
from django_mri.models import help_text
from django_mri.models.managers.score import ScoreManager, ScoreQuerySet


class Score(models.Model):
    """
    Represents the :class:`~django_mri.models.metric.Metric` score for some
    brain :class:`~django_mri.models.region.Region` instance derived from a
    particular :class:`~django_analyses.models.run.Run` instance.
    """

    region = models.ForeignKey(
        "django_mri.Region",
        on_delete=models.CASCADE,
        help_text=help_text.SCORE_REGION,
    )
    metric = models.ForeignKey(
        "django_mri.Metric",
        on_delete=models.CASCADE,
        help_text=help_text.SCORE_METRIC,
    )
    run = models.ForeignKey(
        "django_analyses.Run",
        on_delete=models.CASCADE,
        help_text=help_text.SCORE_RUN,
    )
    value = models.FloatField(
        blank=False, null=False, help_text=help_text.SCORE_VALUE
    )

    objects = ScoreManager.from_queryset(ScoreQuerySet)()

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            Score string representation
        """
        return f"{self.region} [{self.metric}] = {self.value}"

    def to_series(self) -> pd.Series:
        d = {
            "Run ID": self.run.id,
            "Analysis": self.run.analysis_version.analysis.title,
            "Version": self.run.analysis_version.title,
            "Atlas": self.region.atlas.title,
            "Index": self.region.index,
            "Hemisphere": self.region.hemisphere,
            "Region": self.region.title,
            "Metric": self.metric.title,
            "Score": self.value,
        }
        return pd.Series(d, name=self.id)
