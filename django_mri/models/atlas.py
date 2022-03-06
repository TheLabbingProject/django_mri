"""
Definition of the :class:`Atlas` model.
"""
from django.db import models
from django_mri.models import help_text
from django_mri.models.managers.atlas import AtlasQuerySet


class Atlas(models.Model):
    """
    Represents a particular brain atlas in the database.
    """

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text=help_text.ATLAS_TITLE,
    )
    description = models.TextField(
        blank=True, null=True, help_text=help_text.ATLAS_DESCRIPTION
    )
    symmetric = models.BooleanField(
        default=True,
        blank=False,
        null=False,
        help_text=help_text.ATLAS_SYMMETRIC,
    )

    objects = AtlasQuerySet.as_manager()

    # TODO: Add field to point to file.

    class Meta:
        verbose_name_plural = "Atlases"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            Atlas title
        """
        return self.title
