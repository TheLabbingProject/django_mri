"""
Definition of the
:class:`~django_mri.analysis.interfaces.fmriprep.fmriprep` interface.
"""

import os
from pathlib import Path
from django_mri.utils import get_mri_root
from django.conf import settings

COMMAND = "singularity run --cleanenv -B {bids_parent}:/work -B {destination_parent}:/output -B {freesurfer_license}:/fs_license /my_images/fmriprep-latest.simg /work/{bids_name} /output/{destination_name} {analysis_level} --fs-license-file /fs_license"
NIFTI_ROOT = get_mri_root() / "NIfTI"
# ANALYSIS_ROOT = Path(getattr(settings, "ANALYSIS_BASE_PATH"))
ANALYSIS_ROOT = get_mri_root().parent / "analysis"


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
        "native_T1w": ["fmriprep", "anat", "desc-preproc_T1w.nii.gz"],
        "native_brain_mask": ["fmriprep", "anat", "desc-brain_mask.nii.gz"],
        "native_parcellation": ["fmriprep", "anat", "dseg.nii.gz"],
        "native_csf": ["fmriprep", "anat", "CSF_probseg.nii.gz"],
        "native_gm": ["fmriprep", "anat", "GM_probseg.nii.gz"],
        "native_wm": ["fmriprep", "anat", "WM_probseg.nii.gz"],
        "standard_T1w": [
            "fmriprep",
            "anat",
            "space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
        ],
        "standard_brain_mask": [
            "fmriprep",
            "anat",
            "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        ],
        "standard_parcellation": [
            "fmriprep",
            "anat",
            "space-MNI152NLin*dseg.nii.gz",
        ],
        "standard_csf": [
            "fmriprep",
            "anat",
            "space-MNI152NLin2009cAsym_label-CSF_probseg.nii.gz",
        ],
        "standard_gm": [
            "fmriprep",
            "anat",
            "space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz",
        ],
        "standard_wm": [
            "fmriprep",
            "anat",
            "space-MNI152NLin2009cAsym_label-WM_probseg.nii.gz",
        ],
        "native_to_mni_transform": [
            "fmriprep",
            "anat",
            "from-T1w_to-MNI152NLin2009cAsym__mode-image_xfm.h5",
        ],
        "mni_to_native_transform": [
            "fmriprep",
            "anat",
            "from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5",
        ],
        "native_to_fsnative_transform": [
            "fmriprep",
            "anat",
            "from-T1w_to-fsnative_mode-image_xfm.h5",
        ],
        "fsnative_to_native_transform": [
            "fmriprep",
            "anat",
            "from-fsnative_to-T1w_mode-image_xfm.h5",
        ],
        "smoothwm": ["fmriprep", "anat", "smoowthwm.surf.gii"],
        "pial": ["fmriprep", "anat", "pial.surf.gii"],
        "midthickness": ["fmriprep", "anat", "midthickness.surf.gii"],
        "inflated": ["fmriprep", "anat", "inflated.surf.gii"],
        ## Functionals ##
        "native_boldref": [
            "fmriprep",
            "func",
            "space-T1w_desc-boldref.nii.gz",
        ],
        "native_func_brain_mask": [
            "fmriprep",
            "func",
            "space-T1w_desc-brain_mask.nii.gz",
        ],
        "native_preproc_bold": [
            "fmriprep",
            "func",
            "space-T1w_desc-preproc_bold.nii.gz",
        ],
        "native_aparc_bold": [
            "fmriprep",
            "func",
            "space-T1w_desc-aparcaseg_dseg.nii.gz",
        ],
        "native_aseg_bold": [
            "fmriprep",
            "func",
            "space-T1w_desc-aseg_dseg.nii.gz",
        ],
        "standard_boldref": [
            "fmriprep",
            "func",
            "space-MNI152NLin2009cAsym_desc-boldref.nii.gz",
        ],
        "standard_func_brain_mask": [
            "fmriprep",
            "func",
            "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        ],
        "standard_preproc_bold": [
            "fmriprep",
            "func",
            "space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
        ],
        "standard_aparc_bold": [
            "fmriprep",
            "func",
            "space-MNI152NLin2009cAsym_desc-aparcaseg_dseg.nii.gz",
        ],
        "standard_aseg_bold": [
            "fmriprep",
            "func",
            "space-MNI152NLin2009cAsym_desc-aseg_dseg.nii.gz",
        ],
        "confounds_tsv": ["fmriprep", "func", "desc-confound_timeseries.tsv"],
        "confounds_json": [
            "fmriprep",
            "func",
            "desc-confound_timeseries.json",
        ],
        "freesurfer_T1": ["freesurfer", "mri", "T1.mgz"],
        "freesurfer_rawavg": ["freesurfer", "mri", "rawavg.mgz"],
        "freesurfer_orig": ["freesurfer", "mri", "orig.mgz"],
        "freesurfer_nu": ["freesurfer", "mri", "nu.mgz"],
        "freesurfer_norm": ["freesurfer", "mri", "norm.mgz"],
        "freesurfer_aseg": ["freesurfer", "mri", "aseg.mgz"],
        "freesurfer_aseg_stats": ["freesurfer", "stats", "aseg.stats"],
        "freesurfer_brain": ["freesurfer", "mri", "brain.mgz"],
        "freesurfer_brainmask": ["freesurfer", "mri", "brainmask.mgz"],
        "freesurfer_filled": ["freesurfer", "mri", "filled.mgz"],
        "freesurfer_wm": ["freesurfer", "mri", "wm.mgz"],
        "freesurfer_wmparc": ["freesurfer", "mri", "wmparc.mgz"],
        "freesurfer_wmparc_stats": ["freesurfer", "stats", "wmparc.stats"],
        "freesurfer_BA_stats": ["freesurfer", "stats", "*.BA_exvivo*.stats"],
        ### NEEDS COMPLETION ###
    }

    __version__ = "BETA"

    def __init__(self, **kwargs):
        # self.bids_dir = NIFTI_ROOT.absolute()
        # self.destination = ANALYSIS_ROOT.absolute() / kwargs.pop("destination")
        self.bids_dir, self.destination = self.get_root_dirs()
        self.destination = self.destination / kwargs.pop("destination")
        self.configuration = kwargs

    def get_root_dirs(self) -> list:
        """

        Returns
        -------
        list
            [description]
        """
        from django_mri.utils import get_mri_root
        from django.conf import settings

        return get_mri_root() / "NIfTI", Path(settings.MEDIA_ROOT) / "analysis"

    def find_fs_license(self):
        """
        Return default freesurfer license's path
        """
        return Path(os.getenv("FREESURFER_HOME")) / "license.txt"

    def set_configuration_by_keys(self):
        """
        Builds CLI for fmriprep (via singularity) based on user's specifications
        Returns
        -------
        str
            CLI-compatible command
        """
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

    def generate_command(self) -> str:
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
        if not "fs-license-file" in self.configuration.keys():
            fs_license = self.find_fs_license()
        else:
            fs_license = self.configuration.pop("fs-license-file")
        analysis_level = self.configuration.pop("analysis_level")
        command = COMMAND.format(
            bids_parent=self.bids_dir.parent,
            destination_parent=self.destination.parent,
            bids_name=self.bids_dir.name,
            destination_name=self.destination.name,
            analysis_level=analysis_level,
            freesurfer_license=fs_license,
        )
        return command + self.set_configuration_by_keys()

    def find_output(
        self, destination: Path, partial_output: str, subj_id: str
    ):
        """
        uses the destination and some default dictionary to locate specific output files of *fmriprep*
        Parameters
        ----------
        destination : Path
            Output files destination directory
        partial_output : str
            A string that identifies a specific output
        """
        main_dir, sub_dir, output_id = self.DEFAULT_OUTPUTS.get(partial_output)
        if main_dir == "freesurfer":
            output = [
                f
                for f in destination.rglob(
                    f"{main_dir}/{sub_dir}/*{output_id}"
                )
            ]
        elif main_dir == "fmriprep":
            output = [
                f
                for f in destination.rglob(
                    f"{main_dir}/{sub_dir}/{subj_id}*{output_id}"
                )
            ]
        if output:
            if len(output) == 1:
                return output[0]
            else:
                return output
        else:
            return None

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
        output_dict = {}
        for subj in self.configuration.get("participant_label"):
            output_dict[subj] = {}
            for key in self.DEFAULT_OUTPUTS:
                output_dict[key] = self.find_output(destination, key, subj)
        return output_dict

    def run(self) -> dict:
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
        command = self.generate_command()
        print(command)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run fmriprep!\nExecuted command: {command}"
            )
        return self.generate_output_dict(self.destination)
