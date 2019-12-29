from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.serializers.input.definitions.string_input_definition import (
    StringInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.boolean_input_definition import (
    BooleanInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.file_input_definition import (
    FileInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.integer_input_definition import (
    IntegerInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.float_input_definition import (
    FloatInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.list_input_definition import (
    ListInputDefinitionSerializer,
)
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer

SERIALIZERS = {
    InputDefinitions.STR.value: StringInputDefinitionSerializer,
    InputDefinitions.BLN.value: BooleanInputDefinitionSerializer,
    InputDefinitions.FIL.value: FileInputDefinitionSerializer,
    InputDefinitions.INT.value: IntegerInputDefinitionSerializer,
    InputDefinitions.FLT.value: FloatInputDefinitionSerializer,
    InputDefinitions.LST.value: ListInputDefinitionSerializer,
}


class InputDefinitionSerializer(PolymorphicSerializer):
    class Meta:
        model = InputDefinition
        fields = "__all__"

    def get_serializer(self, input_type: str) -> Serializer:
        try:
            return SERIALIZERS[input_type]
        except KeyError:
            raise ValueError(f'Serializer for "{input_type}" does not exist')

