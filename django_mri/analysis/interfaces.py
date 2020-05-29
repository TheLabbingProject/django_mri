from django_mri.analysis.fsl.fsl_anat import FslAnat
from django_mri.analysis.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import BET, FLIRT, FNIRT, Reorient2Std, SUSAN

interfaces = {
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
    "fslreorient2std": {Reorient2Std().version: Reorient2Std},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "FSL Anatomical Processing Script": {FslAnat.__version__: FslAnat},
    "SUSAN": {SUSAN().version: SUSAN},
    "ReconAll": {ReconAll().version: ReconAll},
}
