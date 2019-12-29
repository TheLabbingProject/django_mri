from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.serializers.output.definitions.file_output_definition import (
    FileOutputDefinitionSerializer,
)
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer

SERIALIZERS = {OutputDefinitions.FIL.value: FileOutputDefinitionSerializer}


class OutputDefinitionSerializer(PolymorphicSerializer):
    class Meta:
        model = OutputDefinition
        fields = "__all__"

    def get_serializer(self, output_type: str) -> Serializer:
        try:
            return SERIALIZERS[output_type]
        except KeyError:
            raise ValueError(f'Serializer for "{output_type}" does not exist')

