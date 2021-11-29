"""
Definition of the :class:`SessionQuerySet` class.
"""
import logging

import pandas as pd
from bokeh.plotting import Figure
from django.db.models import Count
from django.db.models.query import QuerySet
from django_mri.models.managers import logs
from django_mri.plots.session import plot_measurement_by_month
from tqdm import tqdm

#: Session fields to include in an exported DataFrame.
DATAFRAME_FIELDS = (
    "id",
    "subject__id",
    "measurement__title",
    "time",
    "irb",
    "scan_count",
)
#: Column names to use when exporting a Session queryset as a DataFrame.
DATAFRAME_COLUMNS = (
    "ID",
    "Subject ID",
    "Measurement",
    "Time",
    "IRB Approval",
    "Scan Count",
)


class SessionQuerySet(QuerySet):
    """
    :class:`~django.db.models.query.QuerySet` sub-class to be used as a custom
    manager for the :class:`~django_mri.models.session.Session` class.

    Note
    ----
    For more information see `Django's Manager documentation`_.

    .. _Django's Manager documentation:
       https://docs.djangoproject.com/en/3.1/topics/db/managers/#creating-a-manager-with-queryset-methods
    """

    _logger = logging.getLogger("data.mri.session")

    def get_scan_set(self) -> QuerySet:
        """
        Returns a queryset of related :class:`~django_mri.models.scan.Scan`
        instances.

        Returns
        -------
        QuerySet
            Related :class:`~django_mri.models.scan.Scan` instances
        """
        Scan = self.model.scan_set.rel.related_model
        return Scan.objects.filter(session__in=self.all())

    def plot_measurement_by_month(self) -> Figure:
        """
        Returns a Bokeh plot of measurement counts by month.

        Returns
        -------
        Figure
            Measurement definition by month
        """
        return plot_measurement_by_month(self.all())

    def to_dataframe(self) -> pd.DataFrame:
        """
        Export the queryset as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Queryset information
        """
        queryset = self.annotate(scan_count=Count("scan"))
        values = queryset.values(*DATAFRAME_FIELDS)
        df = pd.DataFrame(values)
        df.columns = DATAFRAME_COLUMNS
        return df.set_index("ID").sort_index()

    def convert_to_nifti(
        self,
        force: bool = False,
        persistent: bool = True,
        progressbar: bool = True,
        progressbar_position: int = 0,
    ):
        # Log and return if the queryset is empty.
        if not self.exists():
            abort_log = logs.SESSION_SET_NIFTI_CONVERSION_EMPTY.format()
            self._logger.debug(abort_log)
            return
        # Run chronologically in reverse.
        queryset = self.order_by("-time")
        # Log session queryset conversion start.
        start_log = logs.SESSION_SET_NIFTI_CONVERSION_START.format(
            count=queryset.count()
        )
        self._logger.debug(start_log)
        # Create progressbar if required.
        iterator = (
            tqdm(
                queryset,
                desc="Sessions",
                unit="session",
                position=progressbar_position,
                leave=not progressbar_position,
            )
            if progressbar
            else queryset
        )
        n_converted = 0
        # Convert sessions to NIfTI.
        try:
            for session in iterator:
                session.convert_to_nifti(
                    force=force,
                    persistent=persistent,
                    progressbar=progressbar,
                    progressbar_position=progressbar_position + 1,
                )
                n_converted += 1
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SESSION_SET_NIFTI_CONVERSION_FAILURE.format(
                n_converted=n_converted, n_total=queryset.count(), exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log conversion success.
            success_log = logs.SESSION_SET_NIFTI_CONVERSION_SUCCESS.format(
                count=queryset.count()
            )
            self._logger.debug(success_log)
