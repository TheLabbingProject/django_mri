from django.db.models import Manager
from django_mri.models.sequence_type_definition import SequenceTypeDefinition


class SequenceTypeManager(Manager):
    def from_list(self, sequences: list) -> list:
        output = []
        for seq in sequences:
            sequence_type_args = {
                "title": seq["title"],
                "description": seq["description"],
            }
            sequence_type, _ = self.get_or_create(**sequence_type_args)
            for definition in seq["sequence_definitions"]:
                definition_args = {
                    "scanning_sequence": definition["scanning_sequence"],
                    "sequence_variant": definition["sequence_variant"],
                    "sequence_type": sequence_type,
                }
                SequenceTypeDefinition.objects.get_or_create(**definition_args)
            output.append(sequence_type)
        return output
