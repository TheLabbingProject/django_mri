"""
Definition of the
:class:`~django_mri.analysis.interfaces.fsl.topup.TopupWrapper` class.
"""

from nipype.interfaces.fsl import TOPUP


class TopupWrapper(TOPUP):
    """
    A simple subclass of nipype's :class:`~nipype.interfaces.fsl.TOPUP`
    interface, tweaking the interface's :meth:`__init__` method to make input
    specification easier.
    """

    PHASE_ENCODING_DICT = {"i": "x", "j": "y", "k": "z"}

    def __init__(self, *args, **kwargs):
        """
        Sets the *encoding_direction* and *readout_times* parameter values
        using the provided :class:`~django_mri.models.nifti.NIfTI` instances.
        """

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
        """
        Converts phase encoding values from *i, j, k* to *x, y, z*.

        Parameters
        ----------
        phase_encoding : str
            Phase encoding

        Returns
        -------
        str
            Coverted phase encoding
        """

        for key, value in self.PHASE_ENCODING_DICT.items():
            phase_encoding = phase_encoding.replace(key, value)
        return phase_encoding
