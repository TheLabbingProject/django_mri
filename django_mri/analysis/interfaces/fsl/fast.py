"""
Definition of the :class:`~django_mri.analysis.interfaces.fsl.fast.FastWrapper`
class.
"""

from nipype.interfaces.fsl import FAST


class FastWrapper(FAST):
    """
    A simple subclass of nipype's :class:`~nipype.interfaces.fsl.FAST`
    interface, tweaking the :meth:`~nipype.interfaces.fsl.FAST.run` method's
    output slightly to make output specification easier.
    """

    def run(self, *args, **kwargs) -> dict:
        """
        Edits the returned results dictionary to simplify the output
        specification.

        Returns
        -------
        dict
            FAST results
        """

        results = super().run(*args, **kwargs)
        d = results.outputs.get_traitsfree()
        for i, pv_file in enumerate(d["partial_volume_files"]):
            d[f"partial_volume_{i}"] = pv_file
        del d["partial_volume_files"]
        return d
