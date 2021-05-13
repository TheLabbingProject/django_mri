"""
Definition of the :class:`SessionQuerySet` class.
"""
import pandas as pd
from bokeh.plotting import Figure
from django.db.models import Count
from django.db.models.query import QuerySet
from django_mri.plots.session import plot_measurement_by_month

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
