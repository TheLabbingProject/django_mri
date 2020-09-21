"""
General app utilites.
"""

import pytz
from django.apps import apps
from django.db.models import ObjectDoesNotExist
from django.conf import settings
from pathlib import Path
from datetime import datetime

#: The name of the subdirectory under MEDIA_ROOT in which MRI data will be
#: saved.
DEFAULT_MRI_DIR_NAME = "MRI"

#: The name of the subdirectory under the MRI data root in which DICOM files
#: will be saved.
DEFAULT_DICOM_DIR_NAME = "DICOM"

#: Default identifier for a subject model scans should be related to.
DEFAULT_SUBJECT_MODEL = "research.Subject"

#: Default identifier for a study group model scans should be related to.
DEFAULT_STUDY_GROUP_MODEL = "research.Group"


def get_subject_model():
    """
    Returns the subject model MRI scans should be related to.

    Returns
    -------
    django.db.models.Model
        Subject model
    """

    subject_model = getattr(settings, "SUBJECT_MODEL", DEFAULT_SUBJECT_MODEL)
    return apps.get_model(subject_model, require_ready=False)


def get_group_model():
    """
    Returns the study group model MRI scans should be related to.

    Returns
    -------
    django.db.models.Model
        Study group model
    """

    study_group_model = getattr(
        settings, "STUDY_GROUP_MODEL", DEFAULT_STUDY_GROUP_MODEL
    )
    return apps.get_model(study_group_model, require_ready=False)


def get_mri_root() -> Path:
    """
    Returns the path of the directory in which MRI data should be saved.
    """

    default = Path(settings.MEDIA_ROOT, DEFAULT_MRI_DIR_NAME)
    path = getattr(settings, "MRI_ROOT", default)
    return Path(path)


def get_dicom_root() -> Path:
    """
    Returns the path of the directory in which DICOM data should be saved.
    """

    return get_mri_root() / DEFAULT_DICOM_DIR_NAME


def get_session_by_series(series):
    """
    Returns the appropriate session for the given
    :class:`~django_dicom.models.series.Series` instance.

    Parameters
    ----------
    series : :class:`~django_dicom.models.series.Series`
        DICOM series to infer the session from

    Returns
    -------
    :class:`~django_mri.models.session.Session`
        The appropriate session
    """

    Session = apps.get_model("django_mri", "Session")
    Subject = get_subject_model()

    image = series.image_set.first()
    if image:
        header = image.header.instance
        study_date, study_time = (
            header.get("StudyDate"),
            header.get("StudyTime"),
        )
        session_time = datetime.combine(study_date, study_time).replace(
            tzinfo=pytz.UTC
        )
        try:
            subject = Subject.objects.get(id_number=series.patient.uid)
        # If the subject doesn't exist in the database, create a new session
        # without an associated subject.
        except ObjectDoesNotExist:
            session = Session.objects.create(time=session_time)
        # If the subject does exist, look for an existing session by time.
        else:
            session = subject.mri_session_set.filter(time=session_time).first()
            # If no existing session exists, create one.
            if not session:
                session = Session.objects.create(
                    time=session_time, subject=subject
                )
        return session
