from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class SequenceType(TitleDescriptionModel, TimeStampedModel):
    """
    The purpose of this model is to provide a title and description for
     commonly used sequences, as well as to facilitate queries.
    Each particular sequence is defined as a unique combination of DICOM's
    "*ScanningSequence*" and "*SequenceVariant*" attributes.
    This model is a wrapper for the known combinations.

    """

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

    @property
    def scanning_sequence(self) -> list:
        return [
            scan_seq.scanning_sequence
            for scan_seq in self.sequence_definition_set.all()
        ]

    @property
    def sequence_variant(self) -> list:
        return [
            scan_seq.sequence_variant for scan_seq in self.sequence_definition_set.all()
        ]
