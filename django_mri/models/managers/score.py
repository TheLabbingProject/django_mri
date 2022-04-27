"""
Definition of the :class:`ScoreManager` class.
"""
import pandas as pd
from django.db.models import F, Manager, QuerySet
from django.db.models.aggregates import Avg, StdDev
from django_analyses.models.run import Run
from django_mri.analysis.score.scorers import get_scorer


class ScoreManager(Manager):
    """
    Custom QuerySet methods.
    """

    def from_run(self, run: Run) -> QuerySet:
        """
        Creates :class:`~django_mri.models.score.Score` instances from the
        given *run*. This assumes the *run* instance is associated with an
        analysis version that implements an output parser (see
        :func:`~django_analyses.models.run.Run.parse_output`) and return a
        DataFrame of estimated metric values.

        Parameters
        ----------
        run : Run
            Run instance to extract metric scores from
        Returns
        -------
        QuerySet
            Created or existing score instances for the provided *run*
        """
        scorer = get_scorer(run)
        if scorer:
            return scorer(run)


class ScoreQuerySet(QuerySet):
    def to_dataframe(self) -> pd.DataFrame:
        df = pd.concat([score.to_series() for score in self.all()], axis=1).T
        df = df.dropna(axis=1, how="all")
        if "Region" in df.columns:
            return df.set_index(["Run ID", "Origin", "Atlas", "Hemisphere", "Region", "Metric"], drop=True)["Score"].unstack("Metric")
        return df.set_index(["Run ID", "Origin", "Metric"], drop=True)["Score"].unstack("Metric")

    def _repr_html_(self) -> pd.DataFrame:
        return self.to_dataframe()

    def standardize(self) -> QuerySet:
        average = self.aggregate(Avg("value"))["value__avg"]
        std_dev = self.aggregate(StdDev("value"))["value__stddev"]
        return self.annotate(standardized=(F("value") - average) / std_dev)
