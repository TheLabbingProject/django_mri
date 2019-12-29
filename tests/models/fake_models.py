import pandas as pd
from django_fake_model import models as f
from django.db import models
from django.contrib.postgres.fields import JSONField
# from django.urls import reverse
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from .fake.utils import CustomAttributesProcessor, read_subject_table, snake_case_to_camel_case
from .fake.validators import digits_only, not_future, digits_and_dots_only
from .fake.choices import DominantHand, Sex, Gender


class Fake_Subject(TimeStampedModel, f.FakeModel):

    id_number = models.CharNullField(
        max_length=64, unique=True, validators=[digits_only], blank=True, null=True
    )
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    date_of_birth = models.DateField(
        verbose_name="Date of Birth", blank=True, null=True, validators=[not_future]
    )
    dominant_hand = models.CharField(
        max_length=5, choices=DominantHand.choices(), blank=True, null=True
    )
    sex = models.CharField(max_length=6, choices=Sex.choices(), blank=True, null=True)
    gender = models.CharField(
        max_length=5, choices=Gender.choices(), blank=True, null=True
    )
    custom_attributes = JSONField(blank=True, default=dict)

    def __str__(self) -> str:
        return f"Subject #{self.id}"

    def save(self, *args, **kwargs):
        custom_attributes_processor = CustomAttributesProcessor(self.custom_attributes)
        custom_attributes_processor.validate()
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        """
        Returns a formatted string with the subject's full name (first name
        and then last name).

        Returns
        -------
        str
            Subject's full name
        """

        return f"{self.first_name} {self.last_name}"

    def get_raw_information(self) -> pd.Series:
        subject_table = read_subject_table()
        this_subject = subject_table["Anonymized", "Patient ID"] == self.id_number
        return subject_table[this_subject]["Raw"].squeeze()


class Fake_Dicom(TimeStampedModel, f.FakeModel):
    
    # This dictionairy is used to identify fields that do not represent DICOM
    # header information. These fields will not be updated when calling a derived
    # model's update_fields_from_header() method.
    NOT_HEADER_FIELD = {
        "types": (
            models.OneToOneField,
            models.ForeignKey,
            models.AutoField,
            models.ManyToOneRel,
            models.FileField,
            models.TextField,
        ),
        "names": ("created", "modified"),
    }

    # This dictionary is used to convert field names to pydicom's header keywords.
    # It will be used by the derived classes to update their fields using header
    # information.
    FIELD_TO_HEADER = {}

    class Meta:
        abstract = True

    @classmethod
    def get_header_keyword(cls, field_name: str) -> str:
        """
        Returns the pydicom keyword to return the requested field's value from
        header data. Relies on the derived model's `FIELD_TO_HEADER` class attribute.
        If no matching key is found, will simply return the field's name in
        CamelCase formatting (the formatting of pydicom's header keywords).

        Returns
        -------
        str
            pydicom header keyword.
        """

        camel_case = snake_case_to_camel_case(field_name)
        return cls.FIELD_TO_HEADER.get(field_name, camel_case)

    def is_header_field(self, field: models.Field) -> bool:
        """
        Returns a boolean indicating whether this field represents DICOM header
        information or not.
        
        Parameters
        ----------
        field : models.Field
            The field in question.
        
        Returns
        -------
        bool
            Whether this field represent DICOM header information or not.
        """

        valid_type = not isinstance(field, self.NOT_HEADER_FIELD["types"])
        valid_name = field.name not in self.NOT_HEADER_FIELD["names"]
        return valid_type and valid_name

    def get_header_fields(self) -> list:
        """
        Returns a list of the derived model's fields which represent DICOM header
        information.
        
        Returns
        -------
        list
            Fields representing DICOM header information.
        """

        fields = self._meta.get_fields()
        return [field for field in fields if self.is_header_field(field)]

    # def update_fields_from_header(
    #     self, header: HeaderInformation, exclude: list = []
    # ) -> None:
    #     """
    #     Update model fields from header data. 
        
    #     Parameters
    #     ----------
    #     header : HeaderInformation
    #         DICOM header data.
    #     exclude : list, optional
    #         Field names to exclude (the default is [], which will not exclude any header fields).
    #     """
    #     fields = [
    #         field for field in self.get_header_fields() if field.name not in exclude
    #     ]
    #     for field in fields:
    #         keyword = self.get_header_keyword(field.name)
    #         value = header.get_value(keyword)
    #         setattr(self, field.name, value)


class Fake_Study(Fake_Dicom, f.FakeModel):
    uid = models.CharField(
        max_length=64,
        unique=True,
        validators=[digits_and_dots_only],
        verbose_name="Study UID",
    )
    description = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    FIELD_TO_HEADER = {
        "uid": "StudyInstanceUID",
        "date": "StudyDate",
        "time": "StudyTime",
        "description": "StudyDescription",
    }

    class Meta:
        verbose_name_plural = "Studies"
        indexes = [models.Index(fields=["uid"])]

    def __str__(self) -> str:
        return self.uid


class Fake_Group(TitleDescriptionModel, TimeStampedModel, f.FakeModel):

    study = models.ForeignKey("Fake_Study", on_delete=f.CASCADE)

    class Meta:
        unique_together = ("study", "title")

    def __str__(self) -> str:
        return f"{self.study.title}|{self.title}"
