from django_mri.models.sequence_type_definition import SequenceTypeDefinition
from django_mri.models.sequence_type import SequenceType
from rest_framework import serializers


class SequenceTypeDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    sequence_type = serializers.HyperlinkedIdentityField(
        view_name="mri:sequencetype-detail"
    )
    sequence_id = serializers.PrimaryKeyRelatedField(
        queryset=SequenceType.objects.all(), write_only=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="mri:sequencetypedefinition-detail"
    )

    class Meta:
        model = SequenceTypeDefinition
        fields = (
            "id",
            "title",
            "description",
            "scanning_sequence",
            "sequence_variant",
            "sequence_type",
            "sequence_id",
            "url",
        )

    def create(self, validated_data):
        sequence_type = validated_data.pop("sequence_id")
        sequence_def = SequenceTypeDefinition.objects.create(
            sequence_type=sequence_type, **validated_data
        )
        return sequence_def

