from pathlib import Path

from django.conf import settings
from django_mri.utils import get_bids_dir, get_mri_root


def get_media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def get_bids_root() -> Path:
    MEDIA_ROOT = get_media_root()
    return MEDIA_ROOT / get_bids_dir()


def get_recon_all_export_destination(run) -> Path:
    MRI_ROOT = get_mri_root()
    MEDIA_ROOT = get_media_root()
    BIDS_ROOT = get_bids_root()
    t1_files = [
        i for i in run.input_set.all() if i.definition.key == "T1_files"
    ][0]
    path = Path(t1_files.query_related_instance()[0].path)
    analysis_id = (
        str(run.analysis_version).replace(" ", "_").replace(".", "").lower()
    )
    raw_destination = (
        MRI_ROOT / "derivatives" / analysis_id / path.relative_to(BIDS_ROOT)
    ).relative_to(MEDIA_ROOT)
    return Path(str(raw_destination).split(".")[0])


def get_fmriprep_export_destination(run) -> Path:
    MRI_ROOT = get_mri_root()
    MEDIA_ROOT = get_media_root()
    analysis_id = (
        str(run.analysis_version).replace(" ", "_").replace(".", "").lower()
    )
    participant_label = run.get_input("participant_label")[0]
    return (
        MRI_ROOT / "derivatives" / analysis_id / f"sub-{participant_label}"
    ).relative_to(MEDIA_ROOT)


EXPORT_MUTATORS = {
    "ReconAll": get_recon_all_export_destination,
    "fMRIPrep": get_fmriprep_export_destination,
    "dMRIPrep": get_fmriprep_export_destination,
}
