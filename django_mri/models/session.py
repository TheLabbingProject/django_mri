"""
Definition of the :class:`Session` class.
"""
from django.db import models
from django.db.models import QuerySet
from django_extensions.db.models import TimeStampedModel
from django_mri.models import help_text
from django_mri.models.managers.session import SessionQuerySet
from django_mri.utils import (
    get_group_model,
    get_measurement_model,
    get_study_model,
    get_subject_model,
)

Group = get_group_model()
MeasurementDefinition = get_measurement_model()
Study = get_study_model()
Subject = get_subject_model()


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: The associated `Subject` model (optional).
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="mri_session_set",
        blank=True,
        null=True,
    )

    #: Any other information about this scanning sequence.
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=help_text.SESSION_COMMENTS,
    )

    #: The associated `Measurement` model (optional).
    measurement = models.ForeignKey(
        MeasurementDefinition,
        related_name="mri_session_set",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    #: The date and time in which this scanning sequence began.
    time = models.DateTimeField()

    #: Associated IRB approval.
    irb = models.ForeignKey(
        "django_mri.IrbApproval",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="IRB approval",
    )

    objects = SessionQuerySet.as_manager()

    class Meta:
        ordering = ("-time",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        date = self.time.date()
        if self.subject:
            return f"Subject #{self.subject.id} MRI session from {date}"
        return f"Unclaimed MRI session from {date}"

    def query_study_groups(self, id_only: bool = False) -> QuerySet:
        """
        Returns a queryset of associated study groups.

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of primary keys instead of a queryset, by
            default False

        Returns
        -------
        QuerySet
            Associated study groups
        """
        ids = self.scan_set.values_list("study_groups", flat=True)
        return ids if id_only else Group.objects.filter(id__in=ids)

    def query_procedures(self, id_only: bool = False):
        """
        Returns a queryset of associated experimental procedures based on the
        associated measurement definition (if any).

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of primary keys instead of a queryset, by
            default False

        Returns
        -------
        QuerySet
            Associated experimental procedures
        """
        try:
            procedures = self.measurement.procedure_set.all()
        except AttributeError:
            return []
        else:
            return (
                list(procedures.values_list("id", flat=True))
                if id_only
                else procedures
            )

    def query_studies_from_procedures(self, id_only=True) -> QuerySet:
        """
        Returns a queryset of associated studies based on the associated
        measurement definition (if any).

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of primary keys instead of a queryset, by
            default False

        Returns
        -------
        QuerySet
            Associated studies
        """
        procedures = self.query_procedures()
        if procedures:
            ids = list(set(procedures.values_list("study", flat=True)))
            return ids if id_only else Study.objects.filter(id__in=ids)
        return [] if id_only else Study.objects.none()

    def query_studies_from_data(self, id_only: bool = False):
        """
        Returns a queryset of associated studies based on the study group
        relationship with the underlying scans.

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of primary keys instead of a queryset, by
            default False

        Returns
        -------
        QuerySet
            Associated studies from data
        """
        groups = self.query_study_groups()
        ids = list(set(groups.values_list("study", flat=True)))
        return ids if id_only else Study.objects.filter(id__in=ids)

    def query_studies(self, id_only: bool = False):
        """
        Returns a queryset of associated studies.

        Parameters
        ----------
        id_only : bool, optional
            Whether to return a list of primary keys instead of a queryset, by
            default False

        Returns
        -------
        QuerySet
            Associated study groups
        """
        procedure_studies = self.query_studies_from_procedures(id_only=True)
        scan_studies = self.query_studies_from_data(id_only=True)
        ids = procedure_studies + scan_studies
        return ids if id_only else Study.objects.filter(id__in=ids)

    @property
    def study_groups(self) -> QuerySet:
        """
        The experimental groups with which scans in this session are
        associated. This property is only relevant if `STUDY_GROUP_MODEL` is
        set in the project's settings.

        Returns
        -------
        QuerySet
            The associated study groups
        """
        return self.query_study_groups(id_only=False)

    @property
    def subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the session
        acquisition. If the subject's date of birth or the session's
        acquisition time are not available, returns `None`.

        Returns
        -------
        float
            Subject age in years at the time of the session's acquisition
        """

        conditions = self.time and self.subject and self.subject.date_of_birth
        if conditions:
            delta = self.time.date() - self.subject.date_of_birth
            return delta.total_seconds() / (60 * 60 * 24 * 365)

    @property
    def n_scans(self) -> int:
        """
        Returns the number of scans included in this scanning session.

        Returns
        -------
        int
            Number of scan included in this scanning session
        """
        return self.scan_set.count()
