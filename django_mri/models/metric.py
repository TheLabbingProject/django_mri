"""
Definition of the :class:`Metric` model.
"""
from django.db import models
from django_mri.models import help_text


class Metric(models.Model):
    """
    Represents a particular metric of brain anatomy or function in the
    database.
    """

    title = models.CharField(
        max_length=255, blank=True, null=True, help_text=help_text.METRIC_TITLE
    )
    description = models.TextField(
        blank=True, null=True, help_text=help_text.METRIC_DESCRIPTION
    )

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            Metric title
        """
        return self.title
