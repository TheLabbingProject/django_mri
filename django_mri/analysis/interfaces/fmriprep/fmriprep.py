"""
Definition of the
:class:`~django_mri.analysis.interfaces.fmriprep.fmriprep` interface.
"""

import os
from pathlib import Path


class fMRIprep:
    """
    An interface for the *fMRIPrep* preprocessing pipeline.

    References
    ----------
    * fmriprep_

    .. _fmriprep:
       https://fmriprep.org/en/stable/index.html
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.
    FLAGS = (
        "skip_bids_validation",
        "low-mem",
        "anat-only",
        "boilerplate_only",
        "md-only-boilerplate",
        "error-on-aroma-warnings",
        "longitudinal",
        "force-bbr",
        "force-no-bbr",
        "medial-surface-nan",
        "use-aroma",
        "return-all-components",
        "skull-strip-fixed-seed",
        "fmap-bspline",
        "fmap-no-demean",
        "use-syn-sdc",
        "force-syn",
        "no-submm-recon",
        "fs-no-reconall",
        "clean-workdir",
        "resource-monitor",
        "reports-only",
        "write-graph",
        "stop-on-first-crash",
        "notrack",
        "sloppy",
    )

    # Outputs
    DEFAULT_OUTPUTS = {
        ## Anatomicals ##
        "native_T1w": ["anat", "desc-preproc_T1w.nii.gz"],
        "native_brain_mask": ["anat", "desc-brain_mask.nii.gz"],
        "native_parcellation": ["anat", "dseg.nii.gz"],
        "native_csf": ["anat", "CSF_probseg.nii.gz"],
        "native_gm": ["anat", "GM_probseg.nii.gz"],
        "native_wm": ["anat", "WM_probseg.nii.gz"],
        "standard_T1w": [
            "anat",
            "space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
        ],
        "standard_brain_mask": [
            "anat",
            "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        ],
        "standard_parcellation": ["anat", "space-MNI152NLin*dseg.nii.gz"],
        "standard_csf": [
            "anat",
            "space-MNI152NLin2009cAsym_label-CSF_probseg.nii.gz",
        ],
        "standard_gm": [
            "anat",
            "space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz",
        ],
        "standard_wm": [
            "anat",
            "space-MNI152NLin2009cAsym_label-WM_probseg.nii.gz",
        ],
        "native_to_mni_transform": [
            "anat",
            "from-T1w_to-MNI152NLin2009cAsym__mode-image_xfm.h5",
        ],
        "mni_to_native_transform": [
            "anat",
            "from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5",
        ],
        "native_to_fsnative_transform": [
            "anat",
            "from-T1w_to-fsnative_mode-image_xfm.h5",
        ],
        "fsnative_to_native_transform": [
            "anat",
            "from-fsnative_to-T1w_mode-image_xfm.h5",
        ],
        "smoothwm": ["anat", "smoowthwm.surf.gii"],
        "pial": ["anat", "pial.surf.gii"],
        "midthickness": ["anat", "midthickness.surf.gii"],
        "inflated": ["anat", "inflated.surf.gii"],
        ## Functionals ##
        "native_boldref": ["func", "space-T1w_desc-boldref.nii.gz"],
        "native_func_brain_mask": ["func", "space-T1w_desc-brain_mask.nii.gz"],
        "native_preproc_bold": ["func", "space-T1w_desc-preproc_bold.nii.gz"],
        "native_aparc_bold": ["func", "space-T1w_desc-aparcaseg_dseg.nii.gz"],
        "native_aseg_bold": ["func", "space-T1w_desc-aseg_dseg.nii.gz"],
        "standard_boldref": [
            "func",
            "space-MNI152NLin2009cAsym_desc-boldref.nii.gz",
        ],
        "standard_func_brain_mask": [
            "func",
            "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        ],
        "standard_preproc_bold": [
            "func",
            "space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
        ],
        "standard_aparc_bold": [
            "func",
            "space-MNI152NLin2009cAsym_desc-aparcaseg_dseg.nii.gz",
        ],
        "standard_aseg_bold": [
            "func",
            "space-MNI152NLin2009cAsym_desc-aseg_dseg.nii.gz",
        ],
    }

    __version__ = "BETA"

    def __init__(self, **kwargs):
        self.configuration = kwargs

    def set_configuration_by_keys(self):
        key_command = ""
        for key, value in self.configuration.items():
            key_addition = f" --{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            elif key in self.FLAGS and value:
                pass
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self, bids_dir: Path, destination: Path) -> str:
        """
        Returns the command to be executed in order to run the analysis.
        Parameters
        ----------
        bids_dir : Path
            Path to BIDS-appropriate directory
        destination : Path
            Path to output directory

        Returns
        -------
        str
            Complete execution command
        """

        # output_path = destination / self.DEFAULT_OUTPUT_NAME
        analysis_level = self.configuration.pop("analysis_level")
        command = f"singularity run --cleanenv -B {bids_dir.parent}:/work -B {destination.parent}:/output /my_images/fmriprep-latest.simg /work/{bids_dir.name} /output/{destination.name} {analysis_level}"
        return command + self.set_configuration_by_keys()

    def find_output(self, destination: Path, partial_output: str):
        """
        uses the destination and some default dictionary to locate specific output files of *fmriprep*
        Parameters
        ----------
        destination : Path
            Output files destination directory
        partial_output : str
            A string that identifies a specific output
        """
        sub_dir, output_id = partial_output.split("/")
        output = [f for f in destination.rglob(f"{sub_dir}/*{output_id}")]

    def generate_output_dict(self, destination: Path) -> dict:
        """
        Generates a dictionary of the expected output file paths by key.

        Parameters
        ----------
        destination : Path
            Output files destination directory

        Returns
        -------
        dict
            Output files by key
        """

        output_dict = {
            "preprocessed_dwi": destination / self.DEFAULT_OUTPUT_NAME,
        }
        for key, value in self.EDDY_OUTPUTS.items():
            output_dict[key] = destination / value
        return output_dict

    def run(self, bids_dir: Path, destination: Path = None) -> dict:
        """
        Runs *fmriprep* with the provided *bids_dir* as input.
        If *destination* is not specified, output files will be created within
        *bids_dir*\'s parent directory.

        Parameters
        ----------
        bids_dir : Path,
            Path to BIDS-appropriate directory
        destination : Path, optional
            Path to output directory, by default None

        Returns
        -------
        dict
            [Dictionary with keys and values corresponding to descriptions and files of *fmriprep*\'s outputs accordingly]

        Raises
        ------
        RuntimeError
            [In case of failed execution, raises an appropriate error.]
        """

        destination = (
            Path(destination)
            if destination
            else Path(bids_dir).parent / "derivatives"
        )
        command = self.generate_command(bids_dir, destination)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run fmriprep!\nExecuted command: {command}"
            )
        return self.generate_output_dict(destination)
