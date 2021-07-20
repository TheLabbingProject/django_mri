"""
This module exposes a list of preconfigured analyses that may easily be
imported to the database using
:meth:`~django_analyses.models.managers.analysis.AnalysisManager.from_list`.

Example
-------

.. code-block:: py

    from django_analyses.models.analysis import Analysis
    from django_mri.analysis.analysis_definitions import analysis_definitions

    Analysis.objects.from_list(analysis_definitions)

"""
import warnings

import nipype
from django.conf import settings
from django_mri.analysis import messages
from django_mri.analysis.interfaces.fmriprep.fmriprep import (
    FmriPrep2021,
    FmriPrep2022,
)
from django_mri.analysis.interfaces.fsl.fsl_anat import FslAnat
from django_mri.analysis.interfaces.mrtrix3.dwi2tensor import Dwi2Tensor
from django_mri.analysis.interfaces.mrtrix3.dwifslpreproc import DwiFslPreproc
from django_mri.analysis.interfaces.mrtrix3.dwigradcheck import DwiGradCheck
from django_mri.analysis.interfaces.mrtrix3.mrcat import MRCat
from django_mri.analysis.interfaces.mrtrix3.mrconvert import MRConvert
from django_mri.analysis.interfaces.mrtrix3.tensor2metric import Tensor2metric
from django_mri.analysis.specifications.fmriprep.fmriprep import (
    FMRIPREP_INPUT_SPECIFICATION,
    FMRIPREP_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.freesurfer.recon_all import (
    RECON_ALL_INPUT_SPECIFICATION,
    RECON_ALL_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.apply_topup import (
    APPLY_TOPUP_INPUT_SPECIFICATION,
    APPLY_TOPUP_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.binary_maths import (
    BINARY_MATHS_INPUT_SPECIFICATION,
    BINARY_MATHS_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.eddy import (
    EDDY_INPUT_SPECIFICATION,
    EDDY_OUTPUT_SPECIFICATION,
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
from django_mri.analysis.specifications.fsl.fslmerge import (
    FSLMERGE_INPUT_SPECIFICATION,
    FSLMERGE_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.fslroi import (
    FSLROI_INPUT_SPECIFICATION,
    FSLROI_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.fsl.mean_image import (
    MEAN_IMAGE_INPUT_SPECIFICATION,
    MEAN_IMAGE_OUTPUT_SPECIFICATION,
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
from django_mri.analysis.specifications.fsl.topup import (
    TOPUP_INPUT_SPECIFICATION,
    TOPUP_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.bias_correct import (
    BIAS_CORRECT_INPUT_SPECIFICATION,
    BIAS_CORRECT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.compute_metrics import (
    TENSOR2METRIC_OUTPUT_SPECIFICATION,
    TENSOR2METRICS_INPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.degibbs import (
    DEGIBBS_INPUT_SPECIFICATION,
    DEGIBBS_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.denoise import (
    DENOISE_INPUT_SPECIFICATION,
    DENOISE_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.dwifslpreproc import (
    DWIFSLPREPROC_INPUT_SPECIFICATION,
    DWIFSLPREPROC_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.dwigradcheck import (
    DWIGRADCHECK_INPUT_SPECIFICATION,
    DWIGRADCHECK_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.estimate_fod import (
    DWI2FOD_INPUT_SPECIFICATION,
    DWI2FOD_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.estimate_response import (
    DWI2RESPONSE_INPUT_SPECIFICATION,
    DWI2RESPONSE_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.estimate_tensors import (
    DWI2TENSOR_INPUT_SPECIFICATION,
    DWI2TENSOR_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.generate_5tt import (
    GENERATE_5TT_INPUT_SPECIFICATION,
    GENERATE_5TT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.mrcat import (
    MRCAT_INPUT_SPECIFICATION,
    MRCAT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.mrtrix3.mrconvert import (
    MRCONVERT_INPUT_SPECIFICATION,
    MRCONVERT_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.spm.cat12.segmentation import (
    CAT12_SEGMENTATION_INPUT_SPECIFICATION,
    CAT12_SEGMENTATION_OUTPUT_SPECIFICATION,
)
from django_mri.analysis.specifications.yalab.mutual_information_score import (
    MUTUAL_INFORMATION_SCORE_INPUT_SPECIFICATION,
    MUTUAL_INFORMATION_SCORE_OUTPUT_SPECIFICATION,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import (
    BET,
    FAST,
    FLIRT,
    FNIRT,
    SUSAN,
    TOPUP,
    ApplyTOPUP,
    BinaryMaths,
    Eddy,
    ExtractROI,
    MeanImage,
    Merge,
    Reorient2Std,
    RobustFOV,
)
from nipype.interfaces.fsl.base import no_fsl
from nipype.interfaces.mrtrix3 import (
    ConstrainedSphericalDeconvolution,
    DWIBiasCorrect,
    DWIDenoise,
    Generate5tt,
    MRDeGibbs,
    ResponseSD,
)

#: Warn if FSL is not accessible.
test_mode = getattr(settings, "TESTING_MODE", False)
if no_fsl() and not test_mode:
    warnings.warn(messages.NO_FSL)


_NIPYPE_VERSION = nipype.__version__

#: Preconfigured analysis definitions.
analysis_definitions = [
    {
        "title": "BET",
        "description": "FSL brain extraction (BET).",
        "versions": [
            {
                "title": BET().version or "1.0",
                "description": f"Default BET version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": BET_INPUT_SPECIFICATION,
                "output": BET_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "FAST",
        "description": "FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities).",  # noqa: E501
        "versions": [
            {
                "title": FAST().version or "1.0",
                "description": f"Default FAST version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": FAST_INPUT_SPECIFICATION,
                "output": FAST_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "FLIRT",
        "description": "FLIRT (FMRIB's Linear Image Registration Tool) is a fully automated robust and accurate tool for linear (affine) intra- and inter-modal brain image registration.",  # noqa: E501
        "versions": [
            {
                "title": FLIRT().version or "1.0",
                "description": f"Default FLIRT version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
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
                "title": FNIRT().version or "1.0",
                "description": f"Default FNIRT version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": FNIRT_INPUT_SPECIFICATION,
                "output": FNIRT_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "FSL Anatomical Processing Script",
        "description": "A general pipeline for processing anatomical images (e.g. T1-weighted scans).",  # noqa: E501
        "versions": [
            {
                "title": FslAnat.__version__,
                "description": "FSL 6.0 generic anatomical processing script (beta version).",  # noqa: E501
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
                "title": SUSAN().version or "1.0",
                "description": f"Default SUSAN version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": SUSAN_INPUT_SPECIFICATION,
                "output": SUSAN_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "fslmerge",
        "description": "Concatenates images along specified dimension.",
        "versions": [
            {
                "title": Merge().version or "1.0",
                "description": f"Default fslmerge version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": FSLMERGE_INPUT_SPECIFICATION,
                "output": FSLMERGE_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "fslroi",
        "description": "Extracts specific ROI from image.",
        "versions": [
            {
                "title": ExtractROI().version or "1.0",
                "description": f"Default fslroi version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": FSLROI_INPUT_SPECIFICATION,
                "output": FSLROI_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "topup",
        "description": "Estimates and corrects susceptibillity induced distortions.",  # noqa: E501
        "versions": [
            {
                "title": TOPUP().version or "1.0",
                "description": f"Default topup version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": TOPUP_INPUT_SPECIFICATION,
                "output": TOPUP_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "apply_topup",
        "description": "Estimates and corrects susceptibillity induced distortions, following FSL's TopUp fieldmap estimations.",  # noqa: E501
        "versions": [
            {
                "title": ApplyTOPUP().version or "1.0",
                "description": f"Default apply_topup version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": APPLY_TOPUP_INPUT_SPECIFICATION,
                "output": APPLY_TOPUP_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "eddy",
        "description": "estimates and corrects eddy currents induced distortions.",  # noqa: E501
        "versions": [
            {
                "title": Eddy().version or "1.0",
                "description": f"Default eddy version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": EDDY_INPUT_SPECIFICATION,
                "output": EDDY_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "binary_maths",
        "description": "Perform mathematical operations using a second image or a numeric value.",  # noqa: E501
        "versions": [
            {
                "title": BinaryMaths().version or "1.0",
                "description": f"Default BinaryMaths version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": BINARY_MATHS_INPUT_SPECIFICATION,
                "output": BINARY_MATHS_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "mean_image",
        "description": "Generate a mean image across a given dimension.",
        "versions": [
            {
                "title": MeanImage().version or "1.0",
                "description": f"Default MeanImage version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": MEAN_IMAGE_INPUT_SPECIFICATION,
                "output": MEAN_IMAGE_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "fslreorient2std",
        "description": "This is a simple and safe tool designed to reorient an image to match the orientation of the standard template images (MNI152) so that they appear 'the same way around' in FSLView. It requires that the image labels are correct in FSLView before this is run. It is also not a registration tool, so it will not align the image to standard space, it will only apply 90, 180 or 270 degree rotations about the different axes as necessary to get the labels in the same position as the standard template.",  # noqa: E501
        "versions": [
            {
                "title": Reorient2Std().version or "1.0",
                "description": f"Default fslorient2std version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": REORIENT2STD_INPUT_SPECIFICATION,
                "output": REORIENT2STD_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "robustfov",
        "description": "Automatically crops an image removing lower head and neck.",  # noqa: E501
        "versions": [
            {
                "title": RobustFOV().version or "1.0",
                "description": f"Default robustfov version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
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
                "title": "12.7",
                "description": "",
                "fixed_run_method_kwargs": {"verbose_output_dict": True},
                "input": CAT12_SEGMENTATION_INPUT_SPECIFICATION,
                "output": CAT12_SEGMENTATION_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "ReconAll",
        "description": "Performs all, or any part of, the FreeSurfer cortical reconstruction process.",  # noqa: E501
        "versions": [
            {
                "title": ReconAll().version or "1.0",
                "description": f"Default FreeSurfer ReconAll version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": RECON_ALL_INPUT_SPECIFICATION,
                "output": RECON_ALL_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
                "max_parallel": 10,
            }
        ],
    },
    {
        "title": "mrconvert",
        "description": "Performs conversion between different file types and optionally extract a subset of the input image",  # noqa: E501
        "versions": [
            {
                "title": MRConvert.__version__ or "1.0",
                "description": f"Default mrconvert version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": MRCONVERT_INPUT_SPECIFICATION,
                "output": MRCONVERT_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "denoise",
        "description": "Denoise DWI data and estimate the noise level based on the optimal threshold for PCA.",  # noqa: E501
        "versions": [
            {
                "title": DWIDenoise().version or "1.0",
                "description": f"Default dwidenoise version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DENOISE_INPUT_SPECIFICATION,
                "output": DENOISE_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "degibbs",
        "description": "Remove Gibbs ringing artifacts.",
        "versions": [
            {
                "title": MRDeGibbs().version or "1.0",
                "description": f"Default mrdegibbs version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DEGIBBS_INPUT_SPECIFICATION,
                "output": DEGIBBS_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "bias_correct",
        "description": "Perform B1 field inhomogeneity correction for a DWI volume series.",  # noqa: E501
        "versions": [
            {
                "title": DWIBiasCorrect().version or "1.0",
                "description": f"Default dwibiascorrect version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": BIAS_CORRECT_INPUT_SPECIFICATION,
                "output": BIAS_CORRECT_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "dwi2fod",
        "description": "Estimate fibre orientation distributions from diffusion data using spherical deconvolution.",  # noqa: E501
        "versions": [
            {
                "title": ConstrainedSphericalDeconvolution().version or "1.0",
                "description": f"Default ConstrainedSphericalDeconvolution version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DWI2FOD_INPUT_SPECIFICATION,
                "output": DWI2FOD_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "dwi2response",
        "description": "Estimate response function(s) for spherical deconvolution using the specified algorithm.",  # noqa: E501
        "versions": [
            {
                "title": ResponseSD().version or "1.0",
                "description": f"Default ResponseSD version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DWI2RESPONSE_INPUT_SPECIFICATION,
                "output": DWI2RESPONSE_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "5ttgen",
        "description": "Generate a 5TT image suitable for ACT using the selected algorithm.",  # noqa: E501
        "versions": [
            {
                "title": Generate5tt().version or "1.0",
                "description": f"Default Generate5tt version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": GENERATE_5TT_INPUT_SPECIFICATION,
                "output": GENERATE_5TT_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    },
    {
        "title": "dwi2tensor",
        "description": "Convert diffusion-weighted images to tensor images.",  # noqa: E501
        "versions": [
            {
                "title": Dwi2Tensor.__version__ or "1.0",
                "description": f"Default FitTensor version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DWI2TENSOR_INPUT_SPECIFICATION,
                "output": DWI2TENSOR_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "dwifslpreproc",
        "description": "Perform diffusion image pre-processing using FSL’s eddy tool; including inhomogeneity distortion correction using FSL’s topup tool if possible",  # noqa: E501
        "versions": [
            {
                "title": DwiFslPreproc.__version__ or "1.0",
                "description": f"Default dwifslpreproc version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DWIFSLPREPROC_INPUT_SPECIFICATION,
                "output": DWIFSLPREPROC_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "tensor2metric",
        "description": "Generate maps of tensor-derived parameters",  # noqa: E501
        "versions": [
            {
                "title": Tensor2metric.__version__ or "1.0",
                "description": f"Default tensor2metric version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": TENSOR2METRICS_INPUT_SPECIFICATION,
                "output": TENSOR2METRIC_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "mrcat",
        "description": "Concatenate several images into one",  # noqa: E501
        "versions": [
            {
                "title": MRCat.__version__ or "1.0",
                "description": "mrtrix3's mrcat implementation.",  # noqa: E501
                "input": MRCAT_INPUT_SPECIFICATION,
                "output": MRCAT_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "dwigradcheck",
        "description": "Check the orientation of the diffusion gradient table",  # noqa: E501
        "versions": [
            {
                "title": DwiGradCheck.__version__ or "1.0",
                "description": f"Default dwigradcheck version for nipype {_NIPYPE_VERSION}.",  # noqa: E501
                "input": DWIGRADCHECK_INPUT_SPECIFICATION,
                "output": DWIGRADCHECK_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "Mutual Information Score",
        "description": "Calculate mutual information score for two anatomical scans.",  # noqa: E501
        "versions": [
            {
                "title": "1.0",
                "description": "Calculates mutual information using the example from this SO post: https://stackoverflow.com/a/20505476/4416932",  # noqa: E501,
                "input": MUTUAL_INFORMATION_SCORE_INPUT_SPECIFICATION,
                "output": MUTUAL_INFORMATION_SCORE_OUTPUT_SPECIFICATION,
            }
        ],
    },
    {
        "title": "fMRIPrep",
        "description": "A robust preprocessing pipeline for fMRI data.",  # noqa: E501
        "versions": [
            {
                "title": FmriPrep2021.__version__,
                "description": "Flagged version!",  # noqa: E501,
                "input": FMRIPREP_INPUT_SPECIFICATION,
                "output": FMRIPREP_OUTPUT_SPECIFICATION,
            },
            {
                "title": FmriPrep2022.__version__,
                "description": "fMRIprep v20.2.2.",  # noqa: E501,
                "input": FMRIPREP_INPUT_SPECIFICATION,
                "output": FMRIPREP_OUTPUT_SPECIFICATION,
            },
        ],
    },
]
