from pathlib import Path

from django_analyses.models.utils import get_media_root
from django_mri.utils import get_bids_dir, get_mri_root

MEDIA_ROOT = Path(get_media_root())
BIDS_DIR = MEDIA_ROOT / get_bids_dir()
MRI_ROOT = get_mri_root()


def get_recon_all_export_destination(run) -> Path:
    t1_files = [
        i for i in run.input_set.all() if i.definition.key == "T1_files"
    ][0]
    path = Path(t1_files.query_related_instance()[0].path)
    raw_destination = MRI_ROOT / "derivatives" / path.relative_to(BIDS_DIR)
    return Path(str(raw_destination).split(".")[0])


EXPORT_MUTATORS = {"ReconAll": get_recon_all_export_destination}
