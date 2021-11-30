"""
Utilities for the
:class:`~django_mri.analysis.interfaces.qsiprep.qsiprep.QsiPrep` interface.
"""

#: Command line template to format for execution.
COMMAND = "singularity run -e {security_options} -B {bids_parent}:/work,{destination_parent}:/output,{freesurfer_license}:/fs_license {singularity_image_root}/qsiprep-{version}.simg /work/{bids_name} /output/{destination_name} {analysis_level} --fs-license-file /fs_license"  # noqa: E501

#: Default FreeSurfer home directory.
FREESURFER_HOME: str = "/usr/local/freesurfer"

#: "Flags" indicate parameters that are specified without any arguments, i.e.
#: they are a switch for some binary configuration.
FLAGS = (
    "skip_bids_validation",
    "interactive-reports-only",
    "recon-only",
    "low-mem",
    "anat-only",
    "dwi-only",
    "infant",
    "boilerplate",
    "dwi-no-biascorr",
    "no-b0-harmonization",
    "denoise-after-combining",
    "separate_all_dwis",
    "write-local-bvecs",
    "do-reconall",
    "prefer_dedicated_fmaps",
    "fmap-no-demean",
    "use-syn-sdc",
    "force-syn",
    "longitudinal",
    "skull-strip-fixed-seed",
    "fmap-bspline",
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
    "native_T1w": ["qsiprep", "anat", "desc-preproc_T1w.nii.gz"],
    "native_brain_mask": ["qsiprep", "anat", "desc-brain_mask.nii.gz"],
    "native_parcellation": ["qsiprep", "anat", "*dseg.nii.gz"],
    "native_csf": ["qsiprep", "anat", "label-CSF_probseg.nii.gz"],
    "native_gm": ["qsiprep", "anat", "label-GM_probseg.nii.gz"],
    "native_wm": ["qsiprep", "anat", "label-WM_probseg.nii.gz"],
    "standard_T1w": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz",
    ],
    "standard_brain_mask": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
    ],
    "standard_parcellation": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_dseg.nii.gz",
    ],
    "standard_csf": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-CSF_probseg.nii.gz",
    ],
    "standard_gm": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz",
    ],
    "standard_wm": [
        "qsiprep",
        "anat",
        "space-MNI152NLin2009cAsym_label-WM_probseg.nii.gz",
    ],
    "native_to_mni_transform": [
        "qsiprep",
        "anat",
        "from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5",
    ],
    "mni_to_native_transform": [
        "qsiprep",
        "anat",
        "from-MNI152NLin2009cAsym_to-T1w_mode-image_xfm.h5",
    ],
    "native_to_fsnative_transform": [
        "qsiprep",
        "anat",
        "from-T1w_to-fsnative_mode-image_xfm.txt",
    ],
    "fsnative_to_native_transform": [
        "qsiprep",
        "anat",
        "from-fsnative_to-T1w_mode-image_xfm.txt",
    ],
    "smoothwm": ["qsiprep", "anat", "hemi-*_smoothwm.surf.gii"],
    "pial": ["qsiprep", "anat", "hemi-*_pial.surf.gii"],
    "midthickness": ["qsiprep", "anat", "hemi-*_midthickness.surf.gii"],
    "inflated": ["qsiprep", "anat", "hemi-*_inflated.surf.gii"],
    # Diffusion
    "native_dwiref": ["qsiprep", "dwi", "*space-T1w_desc-dwiref.nii.gz"],
    "native_dwi_brain_mask": [
        "qsiprep",
        "dwi",
        "*space-T1w_desc-brain_mask.nii.gz",
    ],
    "native_preproc_dwi": [
        "qsiprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.nii.gz",
    ],
    "native_preproc_bvec": [
        "qsiprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.bvec",
    ],
    "native_preproc_bval": [
        "qsiprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.bval",
    ],
    "native_preproc_mrtrix_grad": [
        "qsiprep",
        "dwi",
        "*space-T1w_desc-preproc_dwi.b",
    ],
    "native_eddy_cnr": ["qsiprep", "dwi", "*space-T1w_desc-eddy_cnr.nii.gz",],
    "native_dwi_qc": ["qsiprep", "dwi", "*dwiqc.json",],
    "native_dwi_sliceqc": ["qsiprep", "dwi", "*desc-SliceQC_dwi.json"],
    "native_dwi_imageqc": ["qsiprep", "dwi", "*desc-ImageQC_dwi.json"],
    "confounds_tsv": ["qsiprep", "dwi", "*_confounds.tsv"],
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
