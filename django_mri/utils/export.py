from pathlib import Path

from django.conf import settings
from django_mri.utils import get_bids_dir, get_mri_root


def get_media_root() -> Path:
    return Path(settings.MEDIA_ROOT)


def get_bids_root() -> Path:
    MEDIA_ROOT = get_media_root()
    return MEDIA_ROOT / get_bids_dir()


def get_recon_all_export_destination(run, path) -> Path:
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
    destintation_dir = Path(str(raw_destination).split(".")[0])
    return destintation_dir / Path(path).relative_to(run.path)


def get_fmriprep_export_destination(run, path) -> Path:
    MRI_ROOT = get_mri_root()
    MEDIA_ROOT = get_media_root()
    analysis_id = (
        str(run.analysis_version).replace(" ", "_").replace(".", "").lower()
    )
    participant_label = run.get_input("participant_label")[0]
    destination_dir = Path(
        str(
            MRI_ROOT / "derivatives" / analysis_id / f"sub-{participant_label}"
        )
    ).relative_to(MEDIA_ROOT)
    return destination_dir / "/".join(
        [
            part
            for part in Path(path).relative_to(run.path).parts[2:]
            if part != "fmriprep"
        ]
    )


def get_dmriprep_export_destination(run, path) -> Path:
    MRI_ROOT = get_mri_root()
    MEDIA_ROOT = get_media_root()
    analysis_id = (
        str(run.analysis_version).replace(" ", "_").replace(".", "").lower()
    )
    participant_label = run.get_input("participant_label")[0]
    destination_dir = Path(
        str(
            MRI_ROOT / "derivatives" / analysis_id / f"sub-{participant_label}"
        )
    ).relative_to(MEDIA_ROOT)
    return destination_dir / "/".join(
        Path(path).relative_to(run.path).parts[2:]
    )


EXPORT_MUTATORS = {
    "ReconAll": get_recon_all_export_destination,
    "fMRIPrep": get_fmriprep_export_destination,
    "dMRIPrep": get_dmriprep_export_destination,
}
