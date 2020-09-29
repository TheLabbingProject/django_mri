import os
from pathlib import Path


def get_fsl_dir():
    return os.getenv("FSLDIR")


def get_template_fa():
    fsldir = Path(get_fsl_dir())
    return fsldir / "data" / "standard" / "FSL_HCP1065_FA_1mm.nii.gz"
