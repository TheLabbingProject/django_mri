from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .managers import SubjectQuerySet


class Subject(TimeStampedModel):
    objects = SubjectQuerySet.as_manager()


class Group(TitleDescriptionModel, TimeStampedModel):
    pass
