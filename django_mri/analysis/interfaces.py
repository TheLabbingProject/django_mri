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


class TopupWrapper(TOPUP):
    PHASE_ENCODING_DICT = {"i": "x", "j": "y", "k": "z"}

    def __init__(self, *args, **kwargs):
        dwi, phasediff = kwargs.pop("dwi_file"), kwargs.pop("phasediff_file")
        kwargs["encoding_direction"] = [
            self.fix_phase_encoding(dwi.get_phase_encoding_direction()),
            self.fix_phase_encoding(phasediff.get_phase_encoding_direction()),
        ]
        kwargs["readout_times"] = [
            dwi.get_total_readout_time(),
            phasediff.get_total_readout_time(),
        ]
        super().__init__(*args, **kwargs)

    def fix_phase_encoding(self, phase_encoding: str) -> str:
        for key, value in self.PHASE_ENCODING_DICT.items():
            phase_encoding = phase_encoding.replace(key, value)
        return phase_encoding


interfaces = {
    "apply_topup": {ApplyTOPUP().version: ApplyTOPUP},
    "binary_maths": {BinaryMaths().version: BinaryMaths},
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
    "fslmerge": {Merge().version: Merge},
    "fslreorient2std": {Reorient2Std().version: Reorient2Std},
    "fslroi": {ExtractROI().version: ExtractROI},
    "FAST": {FAST().version: FastWrapper},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "FSL Anatomical Processing Script": {FslAnat.__version__: FslAnat},
    "mean_image": {MeanImage().version: MeanImage},
    "robustfov": {RobustFOV().version: RobustFOV},
    "ReconAll": {ReconAll().version: ReconAll},
    "SUSAN": {SUSAN().version: SUSAN},
    "topup": {TOPUP().version: TopupWrapper},
}
