from django.db import models
from django_dicom.models import Patient


class SubjectQuerySet(models.QuerySet):
    def from_dicom_patient(self, patient: Patient) -> tuple:
        data = {
            "id_number": patient.uid,
            "first_name": patient.given_name,
            "last_name": patient.family_name,
            "date_of_birth": patient.date_of_birth,
            "sex": patient.sex,
        }
        return self.get_or_create(**data)
