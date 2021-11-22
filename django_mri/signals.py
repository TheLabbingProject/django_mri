"""
Signal receivers.

References
----------
* Signals_

.. _Signals:
   https://docs.djangoproject.com/en/3.0/ref/signals/
"""
import logging
from pathlib import Path

from django.db import IntegrityError
from django.db.models import Model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_dicom.models.series import Series

from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_mri.models.session import Session
from django_mri.utils import get_session_by_series, get_subject_model

_SCAN_FROM_SERIES_FAILURE = (
    "Failed to create Scan instance for DICOM series {series_id}!\n{exception}"
)

_logger = logging.getLogger("data.mri.signals")


@receiver(post_save, sender=Session)
def session_post_save_receiver(
    sender: Model, instance: Session, created: bool, **kwargs
) -> None:
    """
    Creates a new subject automatically if a subject was not assigned and a
    DICOM series is accessible by extracting the
    :class:`~django_dicom.models.patient.Patient` information.

    Parameters
    ----------
    sender : ~django.db.models.Model
        The :class:`~django_mri.models.session.Session` model
    instance : ~django_mri.models.session.Session
        Session instance
    created : bool
        Whether the session instance was created or not
    """
    if not instance.subject:
        Subject = get_subject_model()
        scan = instance.scan_set.first()
        if scan and scan.dicom.patient:
            instance.subject, _ = Subject.objects.from_dicom_patient(
                scan.dicom.patient
            )
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
    session = get_session_by_series(instance)
    if session:
        try:
            scan, created = Scan.objects.get_or_create(
                dicom=instance, session=session
            )
        except IntegrityError:
            # Scan instance already exists in the DB.
            pass
        except Exception as exception:
            message = _SCAN_FROM_SERIES_FAILURE.format(
                series_id=instance.id, exception=exception
            )
            _logger.warning(message)
        else:
            if created:
                session.save()


@receiver(post_delete, sender=NIfTI)
def nifti_post_delete_receiver(
    sender: Model, instance: NIfTI, *args, **kwargs
) -> None:
    """
    Delete files associated with deleted NIfTI instances.

    Parameters
    ----------
    sender : Model
        NIfTI model
    instance : NIfTI
        Deleted NIfTI instance
    """
    path = Path(instance.path)
    if path.exists():
        base_name = path.name.split(".")[0]
        files = path.parent.glob(f"{base_name}.*")
        for f in files:
            f.unlink()
        datatype_dir = path.parent
        session_dir = path.parent.parent
        subject_dir = path.parent.parent.parent
        empty_datatype = not any(datatype_dir.iterdir())
        if empty_datatype:
            datatype_dir.rmdir()
        empty_session = not any(session_dir.iterdir())
        if empty_session:
            session_dir.rmdir()
        empty_subject = not any(subject_dir.iterdir())
        if empty_subject:
            subject_dir.rmdir()
