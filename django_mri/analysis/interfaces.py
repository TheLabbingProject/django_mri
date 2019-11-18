from nipype.interfaces.fsl import BET, FLIRT, FNIRT

interfaces = {
    "BET": {BET().version: BET},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
}
