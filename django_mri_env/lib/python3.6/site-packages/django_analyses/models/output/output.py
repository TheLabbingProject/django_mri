from django.db import models
from model_utils.managers import InheritanceManager


class Output(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run", on_delete=models.CASCADE, related_name="base_output_set"
    )

    value = None
    definition = None

    objects = InheritanceManager()

    def __str__(self) -> str:
        return str(self.value)

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)

    @property
    def key(self) -> str:
        return self.definition.key

