"""
Factories for test models.

Todo
----
* Reintegrate Scan and NIfTI factories.
"""


import factory

from tests.models import Subject


class SubjectFactory(factory.django.DjangoModelFactory):
    # date_of_birth = factory.Faker("date_this_century", before_now=True)
    date_of_birth = factory.Faker("date_this_century", before_today=True)
    sex = factory.Faker("random_element", elements=["M", "F", None])
    dominant_hand = factory.Faker("random_element", elements=["R", "L", None])

    class Meta:
        model = Subject


# class NIfTIFactory(factory.django.DjangoModelFactory):
#     path = factory.Faker("file_path", depth=4, extension="nii.gz")
#     is_raw = factory.Faker("boolean")
#     parent = factory.SubFactory(ScanFactory)

#     class Meta:
#         model = NIfTI
