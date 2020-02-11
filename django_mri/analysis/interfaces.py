from nipype.interfaces.fsl import BET, FLIRT, FNIRT
from django_mri.analysis.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)

interfaces = {
    "BET": {BET().version: BET},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
}
