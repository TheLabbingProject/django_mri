"""
Each analysis version imported to the database using django_analyses_ needs to
have a matching interface registered for it in the project's settings. This
interface is expected to be some class exposing a method (by default
:meth:`run`) which returns a dictionary of outputs matching its associated
:class:`~django_analyses.models.output.output_specification.OutputSpecification`.

References
----------
* `Simplified Analysis Integration Example`_

.. _django_analyses:
   https://github.com/TheLabbingProject/django_analyses
.. _Simplified Analysis Integration Example:
   https://django-analyses.readthedocs.io/en/latest/user_guide/analysis_integration/simplified_example.html
"""
from nipype.interfaces.freesurfer import (
    CALabel,
    MRIsCALabel,
    ParcellationStats,
    ReconAll,
)
from nipype.interfaces.fsl import (
    BET,
    FLIRT,
    FNIRT,
    SUSAN,
    ApplyTOPUP,
    BinaryMaths,
    Eddy,
    ExtractROI,
    MeanImage,
    Merge,
    Reorient2Std,
    RobustFOV,
)
from nipype.interfaces.mrtrix3 import (
    ConstrainedSphericalDeconvolution,
    DWIBiasCorrect,
    DWIDenoise,
    Generate5tt,
    MRDeGibbs,
    ResponseSD,
)

from django_mri.analysis.interfaces.dmriprep.dmriprep import DmriPrep040
from django_mri.analysis.interfaces.fmriprep.fmriprep import (
    FmriPrep2021,
    FmriPrep2022,
    FmriPrep2023,
    FmriPrep2024,
    FmriPrep2025,
    FmriPrep2026,
    FmriPrep2027,
    FmriPrep2100,
    FmriPrep2101,
)
from django_mri.analysis.interfaces.fsl.fast import FastWrapper
from django_mri.analysis.interfaces.fsl.fsl_anat import FslAnat
from django_mri.analysis.interfaces.fsl.topup import TopupWrapper
from django_mri.analysis.interfaces.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)
from django_mri.analysis.interfaces.mriqc.mriqc import MRIQC2100rc2
from django_mri.analysis.interfaces.mrtrix3.dwi2tensor import Dwi2Tensor
from django_mri.analysis.interfaces.mrtrix3.dwifslpreproc import DwiFslPreproc
from django_mri.analysis.interfaces.mrtrix3.dwigradcheck import DwiGradCheck
from django_mri.analysis.interfaces.mrtrix3.mrcat import MRCat
from django_mri.analysis.interfaces.mrtrix3.mrconvert import MRConvert
from django_mri.analysis.interfaces.mrtrix3.tensor2metric import Tensor2metric
from django_mri.analysis.interfaces.qsiprep.qsiprep import QsiPrep0143, QsiPrep0160RC3
from django_mri.analysis.interfaces.yalab.mutual_information_score import (
    MutualInformationScore,
)

#: A dictionary that should be imported in the project's settings and included
#: within the *ANALYSIS_INTERFACES* setting.
interfaces = {
    "apply_topup": {ApplyTOPUP().version: ApplyTOPUP},
    "binary_maths": {BinaryMaths().version: BinaryMaths},
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.7": Cat12Segmentation},
    "fslmerge": {Merge().version: Merge},
    "fslreorient2std": {Reorient2Std().version: Reorient2Std},
    "fslroi": {ExtractROI().version: ExtractROI},
    "FAST": {FastWrapper.version: FastWrapper},
    "FLIRT": {FLIRT().version: FLIRT},
    "FNIRT": {FNIRT().version: FNIRT},
    "FSL Anatomical Processing Script": {FslAnat.__version__: FslAnat},
    "mean_image": {MeanImage().version: MeanImage},
    "robustfov": {RobustFOV().version: RobustFOV},
    "ReconAll": {ReconAll().version: ReconAll},
    "CALabel": {CALabel().version: CALabel},
    "MriSCALabel": {MRIsCALabel().version: MRIsCALabel},
    "AnatomicalStats": {ParcellationStats().version: ParcellationStats},
    "SUSAN": {SUSAN().version: SUSAN},
    "topup": {TopupWrapper.version: TopupWrapper},
    "eddy": {Eddy().version: Eddy},
    "denoise": {DWIDenoise().version: DWIDenoise},
    "degibbs": {MRDeGibbs().version: MRDeGibbs},
    "bias_correct": {DWIBiasCorrect().version: DWIBiasCorrect},
    "dwifslpreproc": {DwiFslPreproc.__version__: DwiFslPreproc},
    "mrconvert": {MRConvert.__version__: MRConvert},
    "dwi2fod": {
        ConstrainedSphericalDeconvolution().version: ConstrainedSphericalDeconvolution  # noqa: E501
    },
    "dwi2response": {ResponseSD().version: ResponseSD},
    "5ttgen": {Generate5tt().version: Generate5tt},
    "dwi2tensor": {Dwi2Tensor.__version__: Dwi2Tensor},
    "tensor2metric": {Tensor2metric.__version__: Tensor2metric},
    "mrcat": {MRCat.__version__: MRCat},
    "dwigradcheck": {DwiGradCheck.__version__: DwiGradCheck},
    "Mutual Information Score": {"1.0": MutualInformationScore},
    "fMRIPrep": {
        FmriPrep2021.__version__: FmriPrep2021,
        FmriPrep2022.__version__: FmriPrep2022,
        FmriPrep2023.__version__: FmriPrep2023,
        FmriPrep2024.__version__: FmriPrep2024,
        FmriPrep2025.__version__: FmriPrep2025,
        FmriPrep2026.__version__: FmriPrep2026,
        FmriPrep2027.__version__: FmriPrep2027,
        FmriPrep2100.__version__: FmriPrep2100,
        FmriPrep2101.__version__: FmriPrep2101,
    },
    "QSIPrep": {
        QsiPrep0143.__version__: QsiPrep0143,
        QsiPrep0160RC3.__version__: QsiPrep0160RC3,
    },
    "dMRIPrep": {DmriPrep040.__version__: DmriPrep040},
    "MRIQC": {MRIQC2100rc2.__version__: MRIQC2100rc2},
}
