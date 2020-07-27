"""
Serializers for the app's models.

References
----------
* Django Rest Framework's `serializers documentation`_.

.. _serializers documentation:
    https://www.django-rest-framework.org/api-guide/serializers/
"""

from django_mri.serializers.nifti import NiftiSerializer
from django_mri.serializers.scan import ScanSerializer
from django_mri.serializers.sequence_type import SequenceTypeSerializer
from django_mri.serializers.sequence_type_definition import (
    SequenceTypeDefinitionSerializer,
)
