from django.db import models
from .utils import CharNullField
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .managers import SubjectQuerySet


class Subject(TimeStampedModel):
    id_number = CharNullField(max_length=64, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    dominant_hand = models.CharField(max_length=5, blank=True, null=True)

    objects = SubjectQuerySet.as_manager()


class Group(TitleDescriptionModel, TimeStampedModel):
    pass
