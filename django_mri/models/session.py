from django_extensions.db.models import TimeStampedModel
from django_mri.models import help_text
from django.db import models


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
        max_length=1000, blank=True, null=True, help_text=help_text.SESSION_COMMENTS,
    )

    def get_scans_avg_acquisition_time(self):
        scans = self.mri_scans.all()
        return scans.aggregate(models.Avg("aquisition_time"))
