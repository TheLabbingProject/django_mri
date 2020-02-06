from django.apps import AppConfig


class DjangoMriConfig(AppConfig):
    name = "django_mri"

    def ready(self):
        import django_mri.signals  # noqa
