from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel

from .managers import SubjectQuerySet
from .utils import CharNullField


class Subject(TimeStampedModel):
    id_number = CharNullField(
        max_length=64, unique=True, blank=True, null=True
    )
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    dominant_hand = models.CharField(max_length=5, blank=True, null=True)

    objects = SubjectQuerySet.as_manager()


class Group(TitleDescriptionModel, TimeStampedModel):
    pass


class MeasurementDefinition(TitleDescriptionModel):
    pass


class Laboratory(TitleDescriptionModel):
    pass
