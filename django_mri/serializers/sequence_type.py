from django_mri.models import SequenceType, SequenceTypeDefinition
from django_mri.serializers.sequence_type_definition import (
    SequenceTypeDefinitionSerializer,
)
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

