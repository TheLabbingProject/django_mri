from django_extensions.db.models import TimeStampedModel

from django_mri.utils import get_subject_model
from django_mri.models import help_text
from django.db import models


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

    time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.scan_set.all():
            self.time = min(self.scan_set.values_list("time", flat=True))
        super().save(*args, **kwargs)
