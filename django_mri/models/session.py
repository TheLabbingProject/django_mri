from django_extensions.db.models import TimeStampedModel
from django.db import models
from django_mri.models import Scan


class Session(TimeStampedModel):
    """
        Represents a scanning session of a specific subject.
    """

    subject = models.ForeignKey(
        "django_mri.Scan",
        on_delete=models.CASCADE,
        related_name="scanning_sessions",
        blank=True,
        null=True,
    )

    comments = models.TextField(
        max_length=1000, blank=True, null=True, help_text=help_text.SCAN_COMMENTS,
    )

