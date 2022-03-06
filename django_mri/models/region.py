"""
Definition of the :class:`Region` model.
"""
from django.db import models
from django.forms import ValidationError
from django_mri.models import help_text
from django_mri.models.choices.hemisphere import Hemisphere
from django_mri.models.managers.region import RegionQuerySet
from django_mri.models.messages import BRAIN_REGION_KEY


class Region(models.Model):
    """
    Represents a particular brain region in the database.
    """

    atlas = models.ForeignKey(
        "django_mri.Atlas",
        on_delete=models.CASCADE,
        help_text=help_text.REGION_ATLAS,
    )
    hemisphere = models.CharField(
        max_length=1,
        choices=Hemisphere.choices(),
        blank=True,
        null=True,
        help_text=help_text.REGION_HEMISPHERE,
    )
    title = models.CharField(
        max_length=255, blank=True, null=True, help_text=help_text.REGION_TITLE
    )
    description = models.TextField(
        blank=True, null=True, help_text=help_text.REGION_DESCRIPTION
    )
    index = models.PositiveIntegerField(
        blank=True, null=True, help_text=help_text.REGION_INDEX
    )
    subcortical = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text=help_text.REGION_SUBCORTICAL,
    )

    objects = RegionQuerySet.as_manager()

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            Region string representation
        """
        if self.hemisphere:
            return f"{self.hemisphere}. {self.title}"
        return self.title

    def validate(self):
        if not (self.title or self.index):
            raise ValidationError(BRAIN_REGION_KEY)

    def save(self, *args, **kwargs):
        self.validate()
        return super().save(*args, **kwargs)
