"""
Definition of the :class:`~django_mri.apps.DjangoMriConfig` class.

References
----------
* `Django applications`_

.. _Django applications:
   https://docs.djangoproject.com/en/3.0/ref/applications/#module-django.apps
"""

from django.apps import AppConfig


class DjangoMriConfig(AppConfig):
    """
    *django_mri* app configuration.

    References
    ----------
    * `AppConfig attributes`_

    .. _AppConfig attributes:
       https://docs.djangoproject.com/en/3.0/ref/applications/#configurable-attributes
    """

    #: Full Python path to the application.
    name = "django_mri"
    bids_manager = None

    def ready(self):
        """
        Loads the app's signals.

        References
        ----------
        * :meth:`~django.apps.AppConfig.ready`
        """
        import django_mri.signals  # noqa: F401
        from django_mri.utils.bids import BidsManager

        self.bids_manager = BidsManager()
        self.bids_manager.initiate_bids_directory()
