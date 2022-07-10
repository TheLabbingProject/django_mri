"""
Utilities for the
:class:`~django_mri.analysis.interfaces.dmriprep.dmriprep.dmriprep` interface.
"""

#: Command line template to format for execution.
COMMAND = "dmriprep {bids_parent}/{bids_name} {destination_parent}/{destination_name} {analysis_level} --fs-license-file {freesurfer_license}"  # noqa: E501

#: Default FreeSurfer home directory.
FREESURFER_HOME: str = "/usr/local/freesurfer"

#: "Flags" indicate parameters that are specified without any arguments, i.e.
#: they are a switch for some binary configuration.
FLAGS = (
    "skip-bids-validation",
    "low-mem",
    "anat-only",
    "boilerplate",
    "longitudinal",
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
    "native_T1w": ["dmriprep", "anat", "desc-preproc_T1w.nii.gz"],
    "native_brain_mask": ["dmriprep", "anat", "desc-brain_mask.nii.gz"],
    "native_parcellation": ["dmriprep", "anat", "*dseg.nii.gz"],
    "native_csf": ["dmriprep", "anat", "label-CSF_probseg.nii.gz"],
    "native_gm": ["dmriprep", "anat", "label-GM_probseg.nii.gz"],
    "native_wm": ["dmriprep", "anat", "label-WM_probseg.nii.gz"],
    "standard_T1w": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
    ],
    "standard_brain_mask": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
    ],
    "standard_parcellation": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_dseg.nii.gz",
    ],
    "standard_csf": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-CSF_probseg.nii.gz",
    ],
    "standard_gm": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz",
    ],
    "standard_wm": [
        "dmriprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-WM_probseg.nii.gz",
    ],
    "native_to_mni_transform": [
        "dmriprep",
        "anat",
        "from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5",
    ],
    "mni_to_native_transform": [
        "dmriprep",
        "anat",
        "from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5",
    ],
    "native_to_fsnative_transform": [
        "dmriprep",
        "anat",
        "from-T1w_to-fsnative_mode-image_xfm.txt",
    ],
    "fsnative_to_native_transform": [
        "dmriprep",
        "anat",
        "from-fsnative_to-T1w_mode-image_xfm.txt",
    ],
    "smoothwm": ["dmriprep", "anat", "hemi-*_smoothwm.surf.gii"],
    "pial": ["dmriprep", "anat", "hemi-*_pial.surf.gii"],
    "midthickness": ["dmriprep", "anat", "hemi-*_midthickness.surf.gii"],
    "inflated": ["dmriprep", "anat", "hemi-*_inflated.surf.gii"],
    # DWI
    "native_dwi_image": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_dwi.nii.gz",
    ],
    "native_dwi_bvec": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_dwi.bvec",
    ],
    "native_dwi_bval": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_dwi.bval",
    ],
    "native_dwi_json": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_dwi.json",
    ],
    "native_dwiref_image": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_epiref.nii.gz",
    ],
    "native_dwiref_json": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-preproc_epiref.json",
    ],
    "coreg_dwi_image": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.nii.gz",
    ],
    "coreg_dwi_bvec": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.bvec",
    ],
    "coreg_dwi_bval": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.bval",
    ],
    "coreg_dwi_json": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.json",
    ],
    "coreg_dwiref_image": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_epiref.nii.gz",
    ],
    "coreg_dwiref_json": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-preproc_epiref.json",
    ],
    "native_dwi_brain_mask": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-brain_mask.nii.gz",
    ],
    "native_preproc_bold": [
        "dmriprep",
        "dwi",
        "*space-dwi_desc-brain_mask.nii.gz",
    ],
    "coreg_preproc_bold": [
        "dmriprep",
        "dwi",
        "*space-T1w_desc-brain_mask.nii.gz",
    ],
    "native_to_anat_transform": [
        "dmriprep",
        "dwi",
        "*from-dwi_to-T1w_mode-image_xfm.txt",
    ],
    "anat_to_native_transform": [
        "dmriprep",
        "dwi",
        "*from-T1w_to-dwi_mode-image_xfm.txt",
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
    "freesurfer_BA_stats": ["freesurfer", "stats", ".BA_exvivo*.stats"],
    # TODO: Finish outputs dictionary.
}
