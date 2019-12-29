from django.conf import settings
from django_analyses.models.output.types.file_output import FileOutput
from rest_framework import serializers


class FileOutputSerializer(serializers.ModelSerializer):
    value = serializers.FilePathField(settings.MEDIA_ROOT)

    class Meta:
        model = FileOutput
        fields = "id", "key", "value", "run", "definition"
