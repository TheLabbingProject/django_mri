from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from django_mri.models.choices import ScanningSequence, SequenceVariant
from django_mri.models.fields import ChoiceArrayField


class SequenceTypeDefinition(TimeStampedModel):
    """
    A model to represent familiar MRI sequences. The purpose of this model is to
    provide a title and description for commonly used sequences, as well as to
    facilitate queries.
    Each particular sequence is defined as a unique combination of DICOM's
    "*ScanningSequence*" and "*SequenceVariant*" attributes.

    """

    scanning_sequence = ChoiceArrayField(
        models.CharField(max_length=2, choices=ScanningSequence.choices()),
        size=5,
        blank=True,
        null=True,
    )
    sequence_variant = ChoiceArrayField(
        models.CharField(max_length=4, choices=SequenceVariant.choices()),
        blank=True,
        null=True,
    )

    sequence_type = models.ForeignKey(
        "django_mri.SequenceType",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sequence_definition_set",
    )

    class Meta:
        unique_together = ("scanning_sequence", "sequence_variant")
        ordering = ("id",)

    def __str__(self) -> str:
        return (
            f"Scanning Sequence: {str(self.scanning_sequence)}\n"
            + f"Sequence Variant: {str(self.sequence_variant)}"
        )
