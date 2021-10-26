"""
Utilities for the
:class:`~django_mri.analysis.interfaces.fmriprep.fmriprep.FmriPrep` interface.
"""

#: Command line template to format for execution.
COMMAND = "singularity run -e {security_options} -B {bids_parent}:/work,{destination_parent}:/output,{freesurfer_license}:/fs_license /my_images/fmriprep-{version}.simg /work/{bids_name} /output/{destination_name} {analysis_level} --fs-license-file /fs_license"  # noqa: E501

#: Default FreeSurfer home directory.
FREESURFER_HOME: str = "/usr/local/freesurfer"

#: "Flags" indicate parameters that are specified without any arguments, i.e.
#: they are a switch for some binary configuration.
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

#: Dictionary of expeected outputs by key.
OUTPUTS = {
    # Anatomicals
    "native_T1w": ["fmriprep", "anat", "desc-preproc_T1w.nii.gz"],
    "native_brain_mask": ["fmriprep", "anat", "desc-brain_mask.nii.gz"],
    "native_parcellation": ["fmriprep", "anat", "*dseg.nii.gz"],
    "native_csf": ["fmriprep", "anat", "label-CSF_probseg.nii.gz"],
    "native_gm": ["fmriprep", "anat", "label-GM_probseg.nii.gz"],
    "native_wm": ["fmriprep", "anat", "label-WM_probseg.nii.gz"],
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
        "space-MNI152NLin2009cAsym_dseg.nii.gz",
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
        "from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5",
    ],
    "mni_to_native_transform": [
        "fmriprep",
        "anat",
        "from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5",
    ],
    "native_to_fsnative_transform": [
        "fmriprep",
        "anat",
        "from-T1w_to-fsnative_mode-image_xfm.txt",
    ],
    "fsnative_to_native_transform": [
        "fmriprep",
        "anat",
        "from-fsnative_to-T1w_mode-image_xfm.txt",
    ],
    "smoothwm": ["fmriprep", "anat", "hemi-*_smoothwm.surf.gii"],
    "pial": ["fmriprep", "anat", "hemi-*_pial.surf.gii"],
    "midthickness": ["fmriprep", "anat", "hemi-*_midthickness.surf.gii"],
    "inflated": ["fmriprep", "anat", "hemi-*_inflated.surf.gii"],
    # Functionals
    "native_boldref": ["fmriprep", "func", "*space-T1w_desc-boldref.nii.gz"],
    "native_func_brain_mask": [
        "fmriprep",
        "func",
        "*space-T1w_desc-brain_mask.nii.gz",
    ],
    "native_preproc_bold": [
        "fmriprep",
        "func",
        "*space-T1w_desc-preproc_bold.nii.gz",
    ],
    "native_aparc_bold": [
        "fmriprep",
        "func",
        "*space-T1w_desc-aparcaseg_dseg.nii.gz",
    ],
    "native_aseg_bold": [
        "fmriprep",
        "func",
        "*space-T1w_desc-aseg_dseg.nii.gz",
    ],
    "standard_boldref": [
        "fmriprep",
        "func",
        "*space-MNI152NLin2009cAsym_desc-boldref.nii.gz",
    ],
    "standard_func_brain_mask": [
        "fmriprep",
        "func",
        "*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
    ],
    "standard_preproc_bold": [
        "fmriprep",
        "func",
        "*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
    ],
    "standard_aparc_bold": [
        "fmriprep",
        "func",
        "*space-MNI152NLin2009cAsym_desc-aparcaseg_dseg.nii.gz",
    ],
    "standard_aseg_bold": [
        "fmriprep",
        "func",
        "*space-MNI152NLin2009cAsym_desc-aseg_dseg.nii.gz",
    ],
    "confounds_tsv": ["fmriprep", "func", "*desc-confound_timeseries.tsv"],
    "confounds_json": ["fmriprep", "func", "*desc-confound_timeseries.json"],
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
    "freesurfer_BA_stats": ["freesurfer", "stats", ".BA_exvivo*.stats"],
    # TODO: Finish outputs dictionary.
}
