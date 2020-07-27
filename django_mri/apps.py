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

    #: Human-readable name for the application.
    verbose_name = "MRI Data Management"

    def ready(self):
        """
        Loads the app's signals.

        References
        ----------
        * :meth:`~django.apps.AppConfig.ready`
        """

        import django_mri.signals  # noqa: F401
