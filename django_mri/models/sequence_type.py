from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from django_mri.models.managers.sequence_type import SequenceTypeManager


class SequenceType(TitleDescriptionModel, TimeStampedModel):
    """
    The purpose of this model is to provide a title and description for
     commonly used sequences, as well as to facilitate queries.
    Each particular sequence is defined as a unique combination of DICOM's
    "*ScanningSequence*" and "*SequenceVariant*" attributes.
    This model is a wrapper for the known combinations.

    """

    objects = SequenceTypeManager()

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation of this instance
        """

        return self.title

    @property
    def sequence_definitions(self) -> list:
        return list(
            self.sequence_definition_set.values(
                "id", "scanning_sequence", "sequence_variant"
            )
        )

