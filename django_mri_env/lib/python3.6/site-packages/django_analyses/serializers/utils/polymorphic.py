"""
Polymorphic serializer class, copied from:
https://stackoverflow.com/questions/48911345/drf-how-to-serialize-models-inheritance-read-write

"""

from enum import Enum
from rest_framework import serializers


class PolymorphicSerializer(serializers.Serializer):
    """
    Serializer to handle multiple subclasses of another class

    - For serialized dict representations, a 'type' key with the class name as
      the value is expected: ex. {'type': 'Decimal', ... }
    - This type information is used in tandem with get_serializer_map(...) to
      manage serializers for multiple subclasses
    """

    def get_serializer(self):
        """
        Return a dict to map class names to their respective serializer classes.
        To be implemented by all PolymorphicSerializer subclasses.
        """

        raise NotImplementedError

    def get_type(self, instance) -> str:
        input_type = (
            instance.get_type()
            if hasattr(instance, "get_type")
            else instance.__class__.__name__
        )
        return input_type.value if isinstance(input_type, Enum) else input_type

    def to_representation(self, instance):
        input_type = self.get_type(instance)
        serializer = self.get_serializer(input_type)
        data = serializer(instance, context=self.context).to_representation(instance)
        data["type"] = input_type
        return data

    def validate_type_key_exists(self, data: dict) -> None:
        if "type" not in data:
            raise serializers.ValidationError({"type": "This field is required"})

    def to_internal_value(self, data):
        self.validate_type_key_exists(data)
        serializer = self.get_serializer(data["type"])
        validated_data = serializer(context=self.context).to_internal_value(data)
        validated_data["type"] = data["type"]
        return validated_data

    def create(self, validated_data):
        serializer = self.get_serializer(validated_data["type"])
        validated_data.pop("type")
        return serializer(context=self.context).create(validated_data)

    def update(self, instance, validated_data):
        serializer = self.get_serializer(validated_data["type"])
        validated_data.pop("type")
        return serializer(context=self.context).update(instance, validated_data)
