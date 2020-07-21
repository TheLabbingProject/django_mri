from django_mri.models.sequence_type import SequenceType
from rest_framework import serializers


class SequenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mri:sequencetype-detail")

    class Meta:
        model = SequenceType
        fields = (
            "id",
            "title",
            "description",
            "sequence_definitions",
            "url",
        )

    def create(self, validated_data):
        sequence_variants = validated_data.pop("sequence_variant")
        scanning_sequences = validated_data.pop("scanning_sequence")
        sequence_type = SequenceType.objects.create(**validated_data)
        return SequenceTypeDefinition.objects.create(
            sequence_variant=sequence_variants,
            scanning_sequence=scanning_sequences,
            sequence_type=sequence_type,
        )

