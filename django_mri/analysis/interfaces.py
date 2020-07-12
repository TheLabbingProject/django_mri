from django_mri.analysis.fsl.fsl_anat import FslAnat
from django_mri.analysis.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import (
    BET,
    FAST,
    FLIRT,
    FNIRT,
    Reorient2Std,
    RobustFOV,
    SUSAN,
    Merge,
    TOPUP,
    ApplyTOPUP,
    MeanImage,
    BinaryMaths,
    ExtractROI,
)


class FastWrapper(FAST):
    def run(self, *args, **kwargs) -> dict:
        results = super().run(*args, **kwargs)
        d = results.outputs.get_traitsfree()
        for i, pv_file in enumerate(d["partial_volume_files"]):
            d[f"partial_volume_{i}"] = pv_file
        del d["partial_volume_files"]
        return d


interfaces = {
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
    "fslreorient2std": {Reorient2Std().version: Reorient2Std},
    "FAST": {FAST().version: FastWrapper},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "fslmerge": {Merge().version: Merge},
    "fslroi": {ExtractROI().version: ExtractROI},
    "topup": {TOPUP().version: TOPUP},
    "apply_topup": {ApplyTOPUP().version: ApplyTOPUP},
    "binary_maths": {BinaryMaths().version: BinaryMaths},
    "mean_image": {MeanImage().version: MeanImage},
    "FSL Anatomical Processing Script": {FslAnat.__version__: FslAnat},
    "SUSAN": {SUSAN().version: SUSAN},
    "ReconAll": {ReconAll().version: ReconAll},
    "robustfov": {RobustFOV().version: RobustFOV},
}
