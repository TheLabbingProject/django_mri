from django_mri.analysis.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import BET, FLIRT, FNIRT

interfaces = {
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "ReconAll": {ReconAll().version: ReconAll},
}
