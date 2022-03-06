"""
Definition of the :class:`AtlasQuerySet` class.
"""
from typing import List

from django.db.models import QuerySet
from django_mri.models.region import Region


class AtlasQuerySet(QuerySet):
    """
    Custom QuerySet methods.
    """

    def from_definition(self, definition: dict):
        regions = definition.pop("regions", [])
        atlas, _ = self.get_or_create(**definition)
        return Region.objects.from_list(atlas, regions)

    def from_list(self, definitions: List[dict]):
        return [self.from_definition(definition) for definition in definitions]
