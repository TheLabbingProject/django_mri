"""
Definition of the :class:`SessionQuerySet` class.
"""

from django.db.models.query import QuerySet


class SessionQuerySet(QuerySet):
    """
    :class:`~django.db.models.query.QuerySet` sub-class to be used as a custom
    manager for the :class:`~django_mri.models.session.Session` class.

    Note
    ----
    For more information see `Django's Manager documentation`_.

    .. _Django's Manager documentation:
       https://docs.djangoproject.com/en/3.1/topics/db/managers/#creating-a-manager-with-queryset-methods
    """

    def get_scan_set(self) -> QuerySet:
        """
        Returns a queryset of related :class:`~django_mri.models.scan.Scan`
        instances.

        Returns
        -------
        QuerySet
            Related :class:`~django_mri.models.scan.Scan` instances
        """

        Scan = self.model.scan_set.rel.related_model
        return Scan.objects.filter(session__in=self.all())
