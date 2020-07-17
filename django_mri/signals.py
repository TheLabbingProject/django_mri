"""
Signal receivers.

References
----------
* Signals_

.. _Signals:
   https://docs.djangoproject.com/en/3.0/ref/signals/
"""

import logging

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_dicom.models.series import Series
from django_mri.models.scan import Scan
from django_mri.utils.get_subject_model import get_subject_model

_SCAN_FROM_SERIES_FAILURE = (
    "Failed to create Scan instance for DICOM series {series_id}!\n{exception}"
)

_logger = logging.getLogger("data.mri.signals")


@receiver(post_save, sender=Scan)
def scan_post_save_receiver(
    sender: Model, instance: Scan, created: bool, **kwargs
) -> None:
    """
    Creates a new subject automatically if a subject was not assigned and a
    DICOM series is accessible by extracting the
    :class:`~django_dicom.models.patient.Patient` information.

    Parameters
    ----------
    sender : ~django.db.models.Model
        The :class:`~django_mri.models.scan.Scan` model
    instance : ~django_mri.models.scan.Scan
        Scan instance
    created : bool
        Whether the scan instance was created or not
    """

    if instance.dicom and not instance.subject:
        Subject = get_subject_model()
        patient = instance.dicom.patient
        if patient:
            instance.subject, _ = Subject.objects.from_dicom_patient(patient)
            instance.save()


@receiver(post_save, sender=Series)
def series_post_save_receiver(
    sender: Model, instance: Series, created: bool, **kwargs
) -> None:
    """
    Create a new :class:`~django_mri.models.scan.Scan` for any created DICOM
    :class:`~django_dicom.models.series.Series` in case one doesn't exist.

    Parameters
    ----------
    sender : ~django.db.models.Model
        The :class:`~django_dicom.models.series.Series` model
    instance : ~django_dicom.models.series.Series
        Series instance
    created : bool
        Whether the series instance was created or not
    """

    try:
        Scan.objects.get_or_create(dicom=instance)
    except Exception as exception:
        message = _SCAN_FROM_SERIES_FAILURE.format(
            series_id=instance.id, exception=exception
        )
        _logger.warning(message)
