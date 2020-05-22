from django.apps import AppConfig


class DjangoMriConfig(AppConfig):
    name = "django_mri"
    verbose_name = "MRI Data Management"

    def ready(self):
        import django_mri.signals  # noqa
