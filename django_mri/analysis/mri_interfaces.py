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

from django_mri.analysis.interfaces.mrtrix3.dwifslpreproc import DwiFslPreproc
from django_mri.analysis.interfaces.matlab.spm.cat12.segmentation import (
    Segmentation as Cat12Segmentation,
)
from django_mri.analysis.interfaces.fsl.fast import FastWrapper
from django_mri.analysis.interfaces.fsl.fsl_anat import FslAnat
from django_mri.analysis.interfaces.fsl.topup import TopupWrapper
from nipype.interfaces.freesurfer import ReconAll
from nipype.interfaces.fsl import (
    BET,
    FLIRT,
    FNIRT,
    Reorient2Std,
    RobustFOV,
    SUSAN,
    Merge,
    ApplyTOPUP,
    MeanImage,
    BinaryMaths,
    ExtractROI,
    Eddy,
)
from nipype.interfaces.mrtrix3 import DWIDenoise, MRDeGibbs, DWIBiasCorrect


#: A dictionary that should be imported in the project's settings and included
#: within the *ANALYSIS_INTERFACES* setting.
interfaces = {
    "apply_topup": {ApplyTOPUP().version: ApplyTOPUP},
    "binary_maths": {BinaryMaths().version: BinaryMaths},
    "BET": {BET().version: BET},
    "CAT12 Segmentation": {"12.6": Cat12Segmentation},
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
    "SUSAN": {SUSAN().version: SUSAN},
    "topup": {TopupWrapper.version: TopupWrapper},
    "eddy": {Eddy().version: Eddy},
    "denoise": {DWIDenoise().version: DWIDenoise},
    "degibbs": {MRDeGibbs().version: MRDeGibbs},
    "bias_correct": {DWIBiasCorrect().version: DWIBiasCorrect},
    "dwipreproc": {DwiFslPreproc.__version__: DwiFslPreproc},
}
