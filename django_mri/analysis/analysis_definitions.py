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
from django_mri.analysis.specifications.fsl.fast import (
    FAST_INPUT_SPECIFICATION,
    FAST_OUTPUT_SPECIFICATION,
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
from django_mri.analysis.specifications.fsl.reorient2std import (
    REORIENT2STD_INPUT_SPECIFICATION,
    REORIENT2STD_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.robustfov import (
    ROBUSTFOV_INPUT_SPECIFICATION,
    ROBUSTFOV_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.susan import (
    SUSAN_INPUT_SPECIFICATION,
    SUSAN_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.spm.cat12.segmentation import (
    CAT12_SEGMENTATION_INPUT_SPECIFICATION,
    CAT12_SEGMENTATION_OUTPUT_SPECIFICATION,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import (
    BET,
    FAST,
    FLIRT,
    FNIRT,
    SUSAN,
    Reorient2Std,
    RobustFOV,
)
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
        "title": "FAST",
        "description": "FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities).",  # noqa
        "versions": [
            {
                "title": FAST().version,
                "description": f"Default FAST version for nipype {nipype.__version__}.",
                "input": FAST_INPUT_SPECIFICATION,
                "output": FAST_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "FLIRT",
        "description": "FLIRT (FMRIB's Linear Image Registration Tool) is a fully automated robust and accurate tool for linear (affine) intra- and inter-modal brain image registration.",  # noqa
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
        "description": "A general pipeline for processing anatomical images (e.g. T1-weighted scans).",  # noqa
        "versions": [
            {
                "title": FslAnat.__version__,
                "description": "FSL 6.0 generic anatomical processing script (beta version).",  # noqa
                "input": FSL_ANAT_INPUT_SPECIFICATION,
                "output": FSL_ANAT_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "SUSAN",
        "description": "Reduces noise in 2/3D images by averaging voxels with similar intensity.",  # noqa
        "versions": [
            {
                "title": SUSAN().version,
                "description": f"Default SUSAN version for nipype {nipype.__version__}.",
                "input": SUSAN_INPUT_SPECIFICATION,
                "output": SUSAN_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "fslreorient2std",
        "description": "This is a simple and safe tool designed to reorient an image to match the orientation of the standard template images (MNI152) so that they appear 'the same way around' in FSLView. It requires that the image labels are correct in FSLView before this is run. It is also not a registration tool, so it will not align the image to standard space, it will only apply 90, 180 or 270 degree rotations about the different axes as necessary to get the labels in the same position as the standard template.",  # noqa
        "versions": [
            {
                "title": Reorient2Std().version,
                "description": f"Default fslorient2std version for nipype {nipype.__version__}.",  # noqa
                "input": REORIENT2STD_INPUT_SPECIFICATION,
                "output": REORIENT2STD_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "robustfov",
        "description": "Automatically crops an image removing lower head and neck.",
        "versions": [
            {
                "title": RobustFOV().version,
                "description": f"Default robustfov version for nipype {nipype.__version__}.",  # noqa
                "input": ROBUSTFOV_INPUT_SPECIFICATION,
                "output": ROBUSTFOV_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
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
        "description": "Performs all, or any part of, the FreeSurfer cortical reconstruction process.",  # noqa
        "versions": [
            {
                "title": ReconAll().version,
                "description": f"Default FreeSurfer ReconAll version for nipype {nipype.__version__}.",  # noqa
                "input": RECON_ALL_INPUT_SPECIFICATION,
                "output": RECON_ALL_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
]
