"""
Utilities for the
:class:`~django_mri.analysis.interfaces.dmriprep.dmriprep.DmriPrep` interface.
"""
from niworkflows.utils.spaces import SpatialReferences, Reference

#: TheBase-specific KWARGS
THE_BASE_BIDS_IDENTIFIERS = dict(
    dwi_identifier={"direction": "ap"},
    fmap_identifier={"acquisition": "dwi"},
    t1w_identifier={"ceagent": "corrected"},
    t2w_identifier={"ceagent": "corrected"},
)

THE_BASE_SMRIPREP_KWARGS = dict(
    freesurfer=True,
    hires=True,
    longitudinal=False,
    omp_nthreads=1,
    skull_strip_mode="force",
    skull_strip_template=Reference("OASIS30ANTs"),
    spaces=SpatialReferences(
        spaces=["MNI152NLin2009cAsym", "fsaverage5", "anat"]
    ),
)

#: Outputs
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
    # dmri
    "native_preproc_dwi_nii": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_dwi.nii.gz",
    ],
    "native_preproc_dwi_json": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_dwi.json",
    ],
    "native_preproc_dwi_bvec": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_dwi.bvec",
    ],
    "native_preproc_dwi_bval": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_dwi.bval",
    ],
    "native_preproc_epi_ref_file": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_epiref.nii.gz",
    ],
    "native_preproc_epiref_json": [
        "dmriprep",
        "dwi",
        "space-orig_desc-preproc_epiref.json",
    ],
    "coreg_preproc_dwi_nii": [
        "dmriprep",
        "dwi",
        "space-anat_desc-preproc_dwi.nii.gz",
    ],
    "coreg_preproc_epiref_nii": [
        "dmriprep",
        "dwi",
        "space-anat_desc-preproc_epiref.nii.gz",
    ],
    "native_to_anat_transform": [
        "dmriprep",
        "dwi",
        "from-epiref_to-T1w_mode-image_xfm.txt",
    ],
    "anat_to_native_transform": [
        "dmriprep",
        "dwi",
        "from-epiref_to-T1w_mode-image_xfm.txt",
    ],
    "phasediff_fmap_nii": [
        "dmriprep",
        "fmap",
        "desc-phasediff_fieldmap.nii.gz",
    ],
    "phasediff_fmap_json": [
        "dmriprep",
        "fmap",
        "desc-phasediff_fieldmap.json",
    ],
    "native_fa": ["dmriprep", "tensor", "space-orig_fa.nii.gz",],
    "native_adc": ["dmriprep", "tensor", "space-orig_adc.nii.gz",],
    "native_ad": ["dmriprep", "tensor", "space-orig_ad.nii.gz",],
    "native_rd": ["dmriprep", "tensor", "space-orig_rd.nii.gz",],
    "native_cl": ["dmriprep", "tensor", "space-orig_cl.nii.gz",],
    "native_cp": ["dmriprep", "tensor", "space-orig_cp.nii.gz",],
    "native_cs": ["dmriprep", "tensor", "space-orig_cs.nii.gz",],
    "native_evec": ["dmriprep", "tensor", "space-orig_evec.nii.gz",],
    "native_eval": ["dmriprep", "tensor", "space-orig_eval.nii.gz",],
    "coreg_fa": ["dmriprep", "tensor", "space-anat_fa.nii.gz",],
    "coreg_adc": ["dmriprep", "tensor", "space-anat_adc.nii.gz",],
    "coreg_ad": ["dmriprep", "tensor", "space-anat_ad.nii.gz",],
    "coreg_rd": ["dmriprep", "tensor", "space-anat_rd.nii.gz",],
    "coreg_cl": ["dmriprep", "tensor", "space-anat_cl.nii.gz",],
    "coreg_cp": ["dmriprep", "tensor", "space-anat_cp.nii.gz",],
    "coreg_cs": ["dmriprep", "tensor", "space-anat_cs.nii.gz",],
    "coreg_evec": ["dmriprep", "tensor", "space-anat_evec.nii.gz",],
    "coreg_eval": ["dmriprep", "tensor", "space-anat_eval.nii.gz",],
    # Freesurfer
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
}
