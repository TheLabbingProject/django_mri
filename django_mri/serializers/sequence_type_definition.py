from django_mri.models.sequence_type_definition import SequenceTypeDefinition
from rest_framework import serializers


class SequenceTypeDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    sequence_type = serializers.HyperlinkedIdentityField(
        view_name="mri:sequencetype-detail"
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
            "url",
        )
