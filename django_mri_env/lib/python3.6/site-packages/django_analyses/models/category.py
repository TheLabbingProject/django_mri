from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Category(TitleDescriptionModel, TimeStampedModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="subcategories",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("title",)
