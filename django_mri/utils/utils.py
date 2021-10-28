"""
General app utilites.
"""

import datetime
from pathlib import Path

import pytz
from django.apps import apps
from django.conf import settings
from django.db.models import ObjectDoesNotExist

#: The name of the subdirectory under MEDIA_ROOT in which MRI data will be
#: saved.
DEFAULT_MRI_DIR_NAME = "MRI"

#: The name of the subdirectory under MEDIA_ROOT in which analyses results will be saved
DEFAULT_ANALYSIS_DIR_NAME = "ANALYSIS"
DEFAULT_ANALYSIS_PATH = Path(settings.MEDIA_ROOT) / DEFAULT_ANALYSIS_DIR_NAME

#: The name of the subdirectory under MEDIA_ROOT in which BIDS dataset will be saved
DEFAULT_BIDS_DIR_NAME = "rawdata"
DEFAULT_BIDS_PATH = Path(settings.MEDIA_ROOT) / DEFAULT_BIDS_DIR_NAME

#: The name of the subdirectory under the MRI data root in which DICOM files
#: will be saved.
DEFAULT_DICOM_DIR_NAME = "DICOM"

#: Default identifier for a subject model scans should be related to.
DEFAULT_SUBJECT_MODEL = "research.Subject"

#: Default identifier for a study model sessions could be related to.
DEFAULT_STUDY_MODEL = "research.Study"

#: Default identifier for a study group model scans should be related to.
DEFAULT_STUDY_GROUP_MODEL = "research.Group"

#: Default identifier for a measurement model sessions should be related to.
DEFAULT_MEASUREMENT_MODEL = "research.MeasurementDefinition"

#: Default value for an MRI data share root directory
DATA_SHARE_ROOT_DEFAULT = "/mnt/"


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


def get_study_model():
    """
    Returns the study model MRI sessions could be related to.

    Returns
    -------
    django.db.models.Model
        Study model
    """

    study_model = getattr(settings, "STUDY_MODEL", DEFAULT_STUDY_MODEL)
    return apps.get_model(study_model, require_ready=False)


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


def get_measurement_model():
    """
    Returns the measurement model MRI sessions should be related to.

    Returns
    -------
    django.db.models.Model
        Measurement model
    """
    measurement_model = getattr(
        settings, "MEASUREMENT_MODEL", DEFAULT_MEASUREMENT_MODEL
    )
    return apps.get_model(measurement_model, require_ready=False)


def get_mri_root() -> Path:
    """
    Returns the path of the directory in which MRI data should be saved.
    """

    default = Path(settings.MEDIA_ROOT, DEFAULT_MRI_DIR_NAME)
    path = getattr(settings, "MRI_ROOT", default)
    return Path(path)


def get_bids_dir() -> Path:
    """
    Returns the path of the directory in which BIDS dataset should be saved.
    """
    path = getattr(settings, "BIDS_BASE_PATH", DEFAULT_BIDS_PATH)
    return Path(path)


def get_analysis_dir() -> Path:
    """
    Returns the path of the directory in which analyses' results should be saved.
    """
    path = getattr(settings, "ANALYSIS_BASE_PATH", DEFAULT_ANALYSIS_PATH)
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
        acquisition_date = header.get("AcquisitionDate")
        instance_date = header.get("InstanceCreationDate", acquisition_date)
        series_date = header.get("SeriesDate", instance_date)
        study_date = header.get("StudyDate", series_date)
        if study_date is not None:
            study_time = header.get("StudyTime", datetime.time())
            session_time = datetime.datetime.combine(
                study_date, study_time
            ).replace(tzinfo=pytz.UTC)
            try:
                subject = Subject.objects.get(id_number=series.patient.uid)
            # If the subject doesn't exist in the database, create a new
            # session without an associated subject.
            except ObjectDoesNotExist:
                session = Session.objects.create(time=session_time)
            # If the subject does exist, look for an existing session by time.
            else:
                session = subject.mri_session_set.filter(
                    time=session_time
                ).first()
                # If no existing session exists, create one.
                if not session:
                    session = Session.objects.create(
                        time=session_time, subject=subject
                    )
                # If a series with the provided number already exists within
                # the session, create a new one (this is mostly relevant when
                # adding multiple subject sessions with no time data).
                else:
                    number_exists = session.scan_set.filter(
                        number=series.number
                    ).exists()
                    if number_exists:
                        session = Session.objects.create(
                            time=session_time, subject=subject
                        )
            return session


def get_data_share_root() -> Path:
    path = getattr(settings, "DATA_SHARE_ROOT", DATA_SHARE_ROOT_DEFAULT)
    return Path(path)
