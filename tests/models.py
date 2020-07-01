from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .managers import SubjectQuerySet


class Subject(TimeStampedModel):
    date_of_birth = models.DateField(blank=True, null=True)
    dominant_hand = models.CharField(
        max_length=5, blank=True, null=True
    )
    sex = models.CharField(max_length=5, blank=True, null=True)

    objects = SubjectQuerySet.as_manager()


class Group(TitleDescriptionModel, TimeStampedModel):
    pass
