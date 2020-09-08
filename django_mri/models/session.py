from django_extensions.db.models import TimeStampedModel
from django.db.models import QuerySet
from django_mri.utils import get_subject_model
from django_mri.models import help_text
from django.db import models
from datetime import datetime


class Session(TimeStampedModel):
    """
        Represents a scanning session of a specific subject.
    """

    subject = models.ForeignKey(
        get_subject_model(),
        on_delete=models.CASCADE,
        related_name="mri_session_set",
        blank=True,
        null=True,
    )

    comments = models.TextField(
        max_length=1000, blank=True, null=True, help_text=help_text.SESSION_COMMENTS,
    )

    time = models.DateTimeField()

    @property
    def study_groups(self) -> QuerySet:
        return self.scan_set.values_list("study_groups", flat=True)
