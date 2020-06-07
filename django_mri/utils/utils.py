from django.apps import apps
from django.conf import settings
from pathlib import Path

DEFAULT_DICOM_DIR_NAME = "DICOM"
DEFAULT_MRI_DIR_NAME = "MRI"


def get_subject_model():
    # app_label, model_name = settings.SUBJECT_MODEL.split(".")
    # return apps.get_model(
    #     app_label=app_label, model_name=model_name, require_ready=False
    # )
    return apps.get_model(settings.SUBJECT_MODEL, require_ready=False)


def get_group_model():
    # app_label, model_name = settings.STUDY_GROUP_MODEL.split(".")
    # return apps.get_model(
    #     app_label=app_label, model_name=model_name, require_ready=False
    # )
    return apps.get_model(settings.STUDY_GROUP_MODEL, require_ready=False)


def get_mri_root() -> Path:
    default = Path(settings.MEDIA_ROOT, DEFAULT_MRI_DIR_NAME)
    path = getattr(settings, "MRI_ROOT", default)
    return Path(path)


def get_dicom_root() -> Path:
    return get_mri_root() / DEFAULT_DICOM_DIR_NAME
