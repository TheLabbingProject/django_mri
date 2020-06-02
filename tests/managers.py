from django.db.models import Manager
from django_dicom.models import Patient


class TestSubjectManager(Manager):
    def from_dicom_patient(self, patient: Patient) -> tuple:
        return self.create(), True
