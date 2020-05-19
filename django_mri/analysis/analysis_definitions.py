import nipype

from django_mri.analysis import messages
from django_mri.analysis.fsl.fsl_anat import FslAnat
from django_mri.analysis.specifications.freesurfer.recon_all import (
    RECON_ALL_INPUT_SPECIFICATION,
    RECON_ALL_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.flirt import (
    FLIRT_INPUT_SPECIFICATION,
    FLIRT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.fnirt import (
    FNIRT_INPUT_SPECIFICATION,
    FNIRT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.fsl_anat import (
    FSL_ANAT_INPUT_SPECIFICATION,
    FSL_ANAT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.spm.cat12.segmentation import (
    CAT12_SEGMENTATION_INPUT_SPECIFICATION,
    CAT12_SEGMENTATION_OUTPUT_SPECIFICATION,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import BET, FLIRT, FNIRT
from nipype.interfaces.fsl.base import no_fsl

if no_fsl():
    raise ImportError(messages.NO_FSL)


analysis_definitions = [
    {
        "title": "BET",
        "description": "FSL brain extraction (BET).",
        "versions": [
            {
                "title": BET().version,
                "description": f"Default BET version for nipype {nipype.__version__}.",
                "input": BET_INPUT_SPECIFICATION,
                "output": BET_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "FLIRT",
        "description": "FLIRT (FMRIB's Linear Image Registration Tool) is a fully automated robust and accurate tool for linear (affine) intra- and inter-modal brain image registration.",
        "versions": [
            {
                "title": FLIRT().version,
                "description": f"Default FLIRT version for nipype {nipype.__version__}.",
                "input": FLIRT_INPUT_SPECIFICATION,
                "output": FLIRT_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "FNIRT",
        "description": "FSL FNIRT wrapper for non-linear registration.",
        "versions": [
            {
                "title": FNIRT().version,
                "description": f"Default FNIRT version for nipype {nipype.__version__}.",
                "input": FNIRT_INPUT_SPECIFICATION,
                "output": FNIRT_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "FSL Anatomical Processing Script",
        "description": "A general pipeline for processing anatomical images (e.g. T1-weighted scans).",
        "versions": [
            {
                "title": FslAnat.__version__,
                "description": "FSL 6.0 generic anatomical processing script (beta version).",
                "input": FSL_ANAT_INPUT_SPECIFICATION,
                "output": FSL_ANAT_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "CAT12 Segmentation",
        "description": "SPM's CAT12 toolkit segmentation.",
        "versions": [
            {
                "title": "12.6",
                "description": "",
                "fixed_run_method_kwargs": {"verbose_output_dict": True},
                "input": CAT12_SEGMENTATION_INPUT_SPECIFICATION,
                "output": CAT12_SEGMENTATION_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "ReconAll",
        "description": "Performs all, or any part of, the FreeSurfer cortical reconstruction process.",
        "versions": [
            {
                "title": ReconAll().version,
                "description": f"Default FreeSurfer ReconAll version for nipype {nipype.__version__}.",
                "input": RECON_ALL_INPUT_SPECIFICATION,
                "output": RECON_ALL_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
]
