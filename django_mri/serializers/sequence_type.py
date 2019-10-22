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
            "scanning_sequence",
            "sequence_variant",
            "url",
        )
