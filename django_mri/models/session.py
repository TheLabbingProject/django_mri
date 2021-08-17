"""
Definition of the :class:`Session` class.
"""
from typing import List

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django_mri.models import help_text
from django_mri.models.managers.session import SessionQueryList
from django_mri.utils import (get_group_model, get_measurement_model,
                              get_study_model, get_subject_model)

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

    objects = SessionQueryList.as_manager()

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
