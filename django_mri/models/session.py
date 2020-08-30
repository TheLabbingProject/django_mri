from django_extensions.db.models import TimeStampedModel
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

    def save(self, *args, **kwargs):
        scans = self.scan_set
        if len(scans.all()) > 0:
            self.time = min(scans.values_list("time", flat=True))
        super().save(*args, **kwargs)
