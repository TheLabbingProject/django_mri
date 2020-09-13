"""
Definition of a custom :class:`~django.db.models.Manager` for the
:class:`~django_mri.tests.models.Subject` model.
"""

from django.db import models
from django_dicom.models import Patient


class SubjectQuerySet(models.QuerySet):
    """
    Custom :class:`~django.db.models.Manager` for the
    :class:`~django_mri.tests.models.Subject` model.
    """

    def from_dicom_patient(self, patient: Patient) -> tuple:
        """
        Gets or creates an :class:`~django_mri.tests.models.Subject` instance
        based on the contents of the provided *.dcm* path.

        Parameters
        ----------
        patient : :class:`~django_dicom.models.patient.Patient`
            Local *.dcm* file path

        Returns
        -------
        Tuple[Subject, bool]
            subject, created
        """

        data = {
            "id_number": patient.uid,
            "first_name": patient.given_name,
            "last_name": patient.family_name,
            "date_of_birth": patient.date_of_birth,
            "sex": patient.sex,
        }
        return self.get_or_create(**data)
