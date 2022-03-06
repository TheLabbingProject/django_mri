"""
Definition of the :class:`ScoreManager` class.
"""
import pandas as pd
from django.db.models import Manager, QuerySet
from django_analyses.models.run import Run
from django_mri.models.atlas import Atlas
from django_mri.models.managers import messages
from django_mri.models.metric import Metric
from django_mri.models.region import Region


def validate_results_df(df: pd.DataFrame, run: Run):
    """
    Checks that the parsed results *df* extracted from *run* is valid.

    Parameters
    ----------
    df : pd.DataFrame
        Parsed results DataFrame
    run : Run
        Run which the parsed results were extracted

    Raises
    ------
    TypeError
        Parsed results not returned as DataFrame
    ValueError
        Empty parsed results
    """
    is_df = isinstance(df, pd.DataFrame)
    if not is_df:
        message = messages.SCORES_BAD_TYPE.format(run)
        raise TypeError(message)
    elif is_df and df.index.nlevels != 3:
        message = messages.SCORES_BAD_INDEX.format(
            run=run, n_levels=df.index.nlevels
        )
    elif is_df and df.empty:
        message = messages.SCORES_EMPTY.format(run=run)
        raise ValueError(message)


def extract_results_df(run: Run):
    df = run.parse_output()
    validate_results_df(df, run)
    return df


class ScoreManager(Manager):
    """
    Custom QuerySet methods.
    """

    def from_run(self, run: Run, force_metrics: bool = False) -> QuerySet:
        """
        Creates :class:`~django_mri.models.score.Score` instances from the
        given *run*. This assumes the *run* instance is associated with an
        analysis version that implements an output parser (see
        :func:`~django_analyses.models.run.Run.parse_output`) and return a
        DataFrame of estimated metric values indexed by (Atlas, Hemisphere,
        Region Name).

        Parameters
        ----------
        run : Run
            Run instance to extract metric scores from
        force_metrics : bool, optional
            Whether to create metrics (i.e. DataFrame columns) that don't exist
            in the databaes, by default False

        Returns
        -------
        QuerySet
            Created or existing score instances for the provided *run*
        """
        df = extract_results_df(run)
        by_metric = df.to_dict()
        score_ids = []
        for metric_title, by_region in by_metric.items():
            try:
                metric = Metric.objects.get(title=metric_title)
            except Metric.DoesNotExist:
                if force_metrics:
                    metric = Metric.objects.create(title=metric_title)
                else:
                    continue
            for key, value in by_region.items():
                atlas_title, hemisphere_label, region_title = key
                atlas, _ = Atlas.objects.get_or_create(title=atlas_title)
                region, _ = Region.objects.get_or_create(
                    atlas=atlas,
                    hemisphere=hemisphere_label[0],
                    title=region_title,
                )
                score, _ = self.get_or_create(
                    run=run, region=region, metric=metric, value=value
                )
                score_ids.append(score.id)
        return self.filter(id__in=score_ids)


class ScoreQuerySet(QuerySet):
    def to_dataframe(self) -> pd.DataFrame:
        return (
            pd.concat([score.to_series() for score in self.all()], axis=1)
            .T.set_index(
                ["Run ID", "Atlas", "Hemisphere", "Region", "Metric"],
                drop=True,
            )["Score"]
            .unstack("Metric")
        )

    def _repr_html_(self) -> pd.DataFrame:
        return self.to_dataframe()
