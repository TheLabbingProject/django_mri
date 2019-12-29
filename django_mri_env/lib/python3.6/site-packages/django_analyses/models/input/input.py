from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager


class Input(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run", on_delete=models.CASCADE, related_name="base_input_set"
    )

    value = None
    definition = None

    objects = InheritanceManager()

    def __str__(self) -> str:
        return str(self.value)

    def raise_required_error(self):
        raise ValidationError(f"{self.key} is required!")

    def pre_save(self) -> None:
        pass

    def validate(self) -> None:
        if self.definition.required and not self.value:
            self.raise_required_error()

    def save(self, *args, **kwargs):
        self.pre_save()
        self.validate()
        super().save(*args, **kwargs)

    @property
    def key(self) -> str:
        return self.definition.key
