"""
Definition of the :class:`~django_mri.analysis.interfaces.fsl.fsl_anat.FslAnat`
class.
"""

import subprocess

from pathlib import Path


class FslAnat:
    """
    Custom interface class for the fsl_anat_ anatomical preprocessing script.

    .. _fsl_anat:
       https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/fsl_anat
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.
    FLAG_ATTRIBUTES = (
        "weak_bias",
        "no_reorient",
        "no_crop",
        "no_bias",
        "no_registration",
        "no_nonlinear_registration",
        "no_segmentation",
        "no_subcortical_segmentation",
        "no_search",
        "no_cleanup",
    )

    #: Conversion dictionary between the verbose names given to the class
    #: initialization keyword arguments and the script's parameters.
    FLAGS = {
        "no_registration": "noreg",
        "no_nonlinear_registration": "nononlinreg",
        "no_segmentation": "noseg",
        "no_subcortical_segmentation": "nosubcortseg",
    }

    #: A suffix given by *fsl_anat* and removed by the interface.
    FORCED_SUFFIX = ".anat"

    #: A dictionary of the file names expected to be created by running the
    #: script.
    OUTPUT_FILES = {
        "linear_registration": "T1_to_MNI_lin.nii.gz",
        "nonlinear_registration": "T1_to_MNI_nonlin.nii.gz",
        "nonlinear_registration_field": "T1_to_MNI_nonlin_field.nii.gz",
        "nonlinear_registration_jacobian": "T1_to_MNI_nonlin_jac.nii.gz",
        "volume_scales": "T1_vols.txt",
        "bias_corrected_brain": "T1_biascorr_brain.nii.gz",
        "bias_corrected_brain_mask": "T1_biascorr_brain_mask.nii.gz",
        "fast_bias_correction": "T1_biascorr.nii.gz",
        "csf_partial_volume": "T1_fast_pve_0.nii.gz",
        "grey_matter_partial_volume": "T1_fast_pve_1.nii.gz",
        "white_matter_partial_volume": "T1_fast_pve_2.nii.gz",
        "segmentation_summary": "T1_fast_pveseg.nii.gz",
        "subcortical_segmentation_summary": "T1_subcort_seg.nii.gz",
    }

    __version__ = "BETA"

    def __init__(
        self,
        weak_bias: bool = False,
        no_reorient: bool = False,
        no_crop: bool = False,
        no_bias: bool = False,
        no_registration: bool = False,
        no_nonlinear_registration: bool = False,
        no_segmentation: bool = False,
        no_subcortical_segmentation: bool = False,
        no_search: bool = False,
        bias_field_smoothing: float = None,
        image_type: str = "T1",
        no_cleanup: bool = False,
    ):
        self.weak_bias = weak_bias
        self.no_reorient = no_reorient
        self.no_crop = no_crop
        self.no_bias = no_bias
        self.no_registration = no_registration
        self.no_nonlinear_registration = no_nonlinear_registration
        self.no_segmentation = no_segmentation
        self.no_subcortical_segmentation = no_subcortical_segmentation
        self.no_search = no_search
        self.bias_field_smoothing = bias_field_smoothing
        self.image_type = image_type
        self.no_cleanup = no_cleanup

    def generate_flags(self) -> str:
        """
        Returns a string containing the various flags configured for this
        instance.

        Returns
        -------
        str
            Execution command flag parameters
        """

        for att_name in self.FLAG_ATTRIBUTES:
            flags = ""
            if getattr(self, att_name):
                default = att_name.replace("_", "")
                flag = self.FLAGS.get(att_name, default)
                flags += f" --{flag}"
            return flags

    def generate_command(self, scan, destination: Path = None) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Parameters
        ----------
        scan : ~django_mri.models.nifti.NIfTI
            The scan to run the analysis on
        destination : Path, optional
            The directory in which output files should be created, by default
            None

        Returns
        -------
        str
            Command string
        """

        flags = self.generate_flags()
        destination_arg = f" -o {str(destination)}" if destination else ""
        return f"fsl_anat {flags} -i {str(scan.path)}{destination_arg}"

    def fix_output_path(self, destination: Path) -> None:
        """
        Removed the forced *.anat* suffix appended to the destination
        directory.

        Parameters
        ----------
        destination : Path
            Destination directory
        """

        destination.with_suffix(self.FORCED_SUFFIX).rename(destination)

    def generate_output_dict(self, destination: Path = None) -> dict:
        """
        Returns a dictionary of the run's output files.

        Parameters
        ----------
        destination : Path, optional
            Destination directory, by default None

        Returns
        -------
        dict
            Output files by key
        """

        self.fix_output_path(destination)
        return {
            key: destination / value
            for key, value in self.OUTPUT_FILES.items()
            if (destination / value).is_file()
        }

    def run(self, scan, destination: Path = None) -> dict:
        """
        Runs *fsl_anat* with the provided *scan* as input and *destination* as
        the destination directory.

        Parameters
        ----------
        scan : ~django_mri.models.nifti.NIfTI
            Input scan
        destination : Path, optional
            Destination directory, by default None

        Returns
        -------
        dict
            Output files by key

        Raises
        ------
        RuntimeError
            Run failure
        """

        destination = (
            Path(destination) if destination else Path(scan.path).parent
        )
        command = self.generate_command(scan, destination).split()
        process = subprocess.run(command, capture_output=True)
        if process.returncode:
            raise RuntimeError("Failed to run fsl_anat!")
        return self.generate_output_dict(destination)
