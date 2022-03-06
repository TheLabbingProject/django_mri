"""
Definition of the :class:`RegionQuerySet` class.
"""
from typing import List

from django.db.models import QuerySet


class RegionQuerySet(QuerySet):
    """
    Custom QuerySet methods.
    """

    def from_definition(self, atlas, definition: dict, symmetric: bool = True):
        """
        Gets or creates a :class:`~django_mri.models.region.Region` instance
        based on the provided *atlas* and *definition*.

        Parameters
        ----------
        atlas : :class:`~django_mri.models.atlas.Atlas`
            Atlas instance
        definition : dict
            Region dictionary definition
        symmetric : bool, optional
            Whether this region should be created for both cerebral
            hemispheres, by default True

        Returns
        -------
        django_mri.models.region.Region
            Existing or created region instance
        """
        symmetric = atlas.symmetric or definition.get("symmetric", False)
        if symmetric:
            definition["hemisphere"] = "L"
            left, _ = self.get_or_create(atlas=atlas, **definition)
            definition["hemisphere"] = "R"
            right, _ = self.get_or_create(atlas=atlas, **definition)
            return left, right
        return self.get_or_create(atlas=atlas, **definition)[0]

    def from_list(self, atlas, definitions: List[dict]):
        """
        Gets or creates a :class:`~django_mri.models.region.Region` instances
        based on the provided *atlas* and *definitions* list.

        Parameters
        ----------
        atlas : :class:`~django_mri.models.atlas.Atlas`
            Atlas instance
        definition : dict
            Region dictionary definitions

        Returns
        -------
        _type_
            _description_
        """
        return [
            self.from_definition(atlas, definition)
            for definition in definitions
        ]
