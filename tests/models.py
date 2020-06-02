from django_extensions.db.models import TitleDescriptionModel
from .managers import TestSubjectManager


class Subject(TitleDescriptionModel):
    objects = TestSubjectManager()


class Group(TitleDescriptionModel):
    pass
