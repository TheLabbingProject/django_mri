from django.db import models
from django_dicom.models import Patient


class SubjectQuerySet(models.QuerySet):
    def from_dicom_patient(self, patient: Patient) -> tuple:
        return self.create(), True
