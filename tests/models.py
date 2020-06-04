from django_extensions.db.models import TitleDescriptionModel
from .managers import SubjectQuerySet


class Subject(TitleDescriptionModel):
    objects = SubjectQuerySet.as_manager()


class Group(TitleDescriptionModel):
    pass
