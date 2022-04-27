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

    origin = models.ManyToManyField(
        "django_mri.Scan", help_text=help_text.SCORE_ORIGIN,
    )
    region = models.ForeignKey(
        "django_mri.Region",
        on_delete=models.CASCADE,
        help_text=help_text.SCORE_REGION,
        blank=True,
        null=True,
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
        if self.region:
            return f"{self.metric} [{self.region}] = {self.value}"
        return f"{self.metric} = {self.value}"

    def to_series(self) -> pd.Series:
        d = {
            "Run ID": self.run.id,
            "Origin": self.origin.values_list("id", flat=True) if self.origin else None,
            "Analysis": self.run.analysis_version.analysis.title,
            "Version": self.run.analysis_version.title,
            "Atlas": self.region.atlas.title if self.region else None,
            "Index": self.region.index if self.region else None,
            "Hemisphere": self.region.hemisphere if self.region else None,
            "Region": self.region.title if self.region else None,
            "Metric": self.metric.title,
            "Score": self.value,
        }
        d["Origin"] = d["Origin"][0] if len(d["Origin"]) == 1 else d["Origin"]
        return pd.Series(d, name=self.id)
