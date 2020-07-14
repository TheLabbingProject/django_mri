from django_mri.models.sequence_type import SequenceType
from rest_framework import serializers


class SequenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    sequence_definition_set = serializers.HyperlinkedIdentityField(
        view_name="mri:sequencetypedefinition-detail"
    )
    url = serializers.HyperlinkedIdentityField(view_name="mri:sequencetype-detail")

    class Meta:
        model = SequenceType
        fields = (
            "id",
            "title",
            "description",
            "sequence_definition_set",
            "scanning_sequence",
            "sequence_variant",
            "url",
        )
