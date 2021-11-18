"""
Input and output specification dictionaries for FreeSurfer's recon_all_ script.

.. _recon_all:
   https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all
"""

from django.conf import settings
from django_analyses.models.input.definitions import (BooleanInputDefinition,
                                                      DirectoryInputDefinition,
                                                      FileInputDefinition,
                                                      FloatInputDefinition,
                                                      IntegerInputDefinition,
                                                      ListInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.output.definitions import (FileOutputDefinition,
                                                       ListOutputDefinition)
from traits.trait_types import String

#: *dmriprep* input specification.
DMRIPREP_INPUT_SPECIFICATION = {
    "destination": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "required": True,
        "description": "Path to output directory",
    },
    ### Options to handle performance ###
    "bids_validate": {
        "type": BooleanInputDefinition,
        "description": "assume the input dataset is BIDS compliant and skip the validation",  # noqa: E501
        "default": True,
    },
    "participant_label": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "required": True,
        "description": "a space delimited list of participant identifiers or a single identifier (the sub- prefix can be removed)",  # noqa: E501
        "is_configuration": False,
    },
    ### Specific options for FreeSurfer preprocessing ###
    "fs_subjects_dir": {
        "type": DirectoryInputDefinition,
        "description": "Path to existing FreeSurfer subjects directory to reuse.",
    },
    "work_dir": {
        "type": DirectoryInputDefinition,
        "description": "path where intermediate results should be stored",
    },
}
#: *dMRIprep* output specification.
DMRIPREP_OUTPUT_SPECIFICATION = {
    # fmriprep
    # native
    # anat/*desc-preproc_T1w.nii.gz
    "native_T1w": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical image in native space.",
    },
    # anat/*desc-brain_mask.nii.gz
    "native_brain_mask": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical brain mask in native space.",
    },
    # anat/*dseg.nii.gz
    "native_parcellation": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical brain parcellation in native space.",
    },
    # anat/*CSF_probseg.nii.gz
    "native_csf": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "CSF mask in native space.",
    },
    # anat/*GM_probseg.nii.gz
    "native_gm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "GM mask in native space.",
    },
    # anat/*WM_probseg.nii.gz
    "native_wm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "WM mask in native space.",
    },
    ## standard
    # anat/*desc-preproc_T1w.nii.gz
    "standard_T1w": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical image in standard space.",
    },
    # anat/*desc-brain_mask.nii.gz
    "standard_brain_mask": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical brain mask in standard space.",
    },
    # anat/*dseg.nii.gz
    "standard_parcellation": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed anatomical brain parcellation in standard space.",
    },
    # anat/*CSF_probseg.nii.gz
    "standard_csf": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "CSF mask in standard space.",
    },
    # anat/*GM_probseg.nii.gz
    "standard_gm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "GM mask in standard space.",
    },
    # anat/*WM_probseg.nii.gz
    "standard_wm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "WM mask in standard space.",
    },
    # anat/*from-T1wto-MNI..._mode-image_xfm.h5
    "native_to_mni_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Transformation file from native to standard space.",
    },
    # anat/*from-MNI...to-T1w_mode-image_xfm.h5
    "mni_to_native_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Transformation file from standard to native space.",
    },
    # anat/*from-fsnative...to-T1w_mode-image_xfm.txt
    "native_to_fsnative_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Transformation file from native to freesurfer's standard space.",
    },
    # anat/*from-fsnative...to-T1w_mode-image_xfm.txt
    "fsnative_to_native_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Transformation file from freesurfer's  standard to native space.",
    },
    ## surfaces
    # anat/*smoothwm.surf.gii
    "smoothwm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Smoothed original surface meshes.",
    },
    # anat/*pial.surf.gii
    "pial": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Gray matter/pia mater surface meshes.",
    },
    # anat/*midthickness.surf.gii
    "midthickness": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Graymid/midthickness surface meshes.",
    },
    # anat/*inflated.surf.gii
    "inflated": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Inflated surface meshes.",
    },
    ## diffusion
    # native
    # preproc
    "native_preproc_dwi_nii": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed dMRI NIfTI series in native space.",
    },
    "native_preproc_dwi_json": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed dMRI's json.",
    },
    "native_preproc_dwi_bvec": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed dMRI's .bvec.",
    },
    "native_preproc_dwi_bval": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed dMRI's .bval.",
    },
    # epi reference
    "native_preproc_epi_ref_nii": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed single volume (EPI reference) NIfTI file.",
    },
    "native_preproc_epiref_json": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed EPI-ref's json.",
    },
    # Coreg
    "coreg_preproc_dwi_nii": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed dMRI NIfTI series in anatomical space.",
    },
    "coreg_preproc_epiref_nii": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed single volume EPI reference NIfTI in anatomical space.",
    },
    # Transforms
    "native_to_anat_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "dMRI-to-anatomical transformation matrix.",
    },
    "anat_to_native_transform": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Anatomical-to-dMRI transformation matrix.",
    },
    # phasediff
    "phasediff_fmap_nii": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Phase-opposite NIfTI file.",
    },
    "phasediff_fmap_json": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Phase-opposite json file.",
    },
    # native tensor-derived metrics
    "native_fa": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Fractional Anisotropy (FA) in native dMRI space.",
    },
    "native_adc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Apperent Diffusion Coefficient (ADC) in native dMRI space.",
    },
    "native_ad": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Axial Diffusivity (AD) in native dMRI space.",
    },
    "native_rd": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Radial Diffusivity (RD) in native dMRI space.",
    },
    "native_cl": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived linearity metric in native dMRI space.",
    },
    "native_cp": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived planarity metric in native dMRI space.",
    },
    "native_cs": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived sphericiry metric in native dMRI space.",
    },
    "native_evec": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived eigenvector(s) in native dMRI space.",
    },
    "native_eval": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived eigenvalue(s) in native dMRI space.",
    },
    # coregistered tensor-derived metrics
    "coreg_fa": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Fractional Anisotropy (FA) in anatomical space.",
    },
    "coreg_adc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Apperent Diffusion Coefficient (ADC) in anatomical space.",
    },
    "coreg_ad": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Axial Diffusivity (AD) in anatomical space.",
    },
    "coreg_rd": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived Radial Diffusivity (RD) in anatomical space.",
    },
    "coreg_cl": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived linearity metric in anatomical space.",
    },
    "coreg_cp": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived planarity metric in anatomical space.",
    },
    "coreg_cs": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived sphericiry metric in anatomical space.",
    },
    "coreg_evec": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived eigenvector(s) in anatomical space.",
    },
    "coreg_eval": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Tensor-derived eigenvalue(s) in anatomical space.",
    },
    # freesurfer/
    # mri/T1.mgz
    "freesurfer_T1": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Intensity normalized whole-head volume.",
    },
    # mri/rawavg.mgz
    "freesurfer_rawavg": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "An average volume of the raw input data (if there is only one input volume, they will be identical). This volume is unconformed (i.e. to 256^3, 1mm isotropic)",  # noqa: E501
    },
    # mri/orig.mgz
    "freesurfer_orig": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "A conformed (i.e. to 256^3, 1mm isotropic) average volume of the raw input data.",
    },
    # mri/nu.mgz
    "freesurfer_nu": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "This is an intensity normalized volume generated after correcting for non-uniformity in conformed raw average (saved as 'mri/orig.mgz'). If there are any errors in later steps, it sometimes helps to check if the intensity values don't look normal in this file. If the values are too high, then scaling down the intensity a little bit and re-running recon-all usually corrects that error. In some cases, this scaling down can also be done for the orig.mgz volume.",  # noqa: E501
    },
    # mri/norm.mgz
    "freesurfer_norm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Normalized skull-stripped volume.",
    },
    # mri/aseg.mgz
    "freesurfer_aseg": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Volumetric map of regions from automatic segmentation.",
    },
    # stats/aseg.stats
    "freesurfer_aseg_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Automated segmentation statistics file.",
    },
    # mri/brain.mgz
    "freesurfer_brain": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Intensity normalized brain-only volume.",
    },
    # mri/brainmask.mgz
    "freesurfer_brainmask": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Skull-stripped (brain-only) volume.",
    },
    # mri/filled.mgz
    "freesurfer_filled": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Subcortical mass volume.",
    },
    # mri/wm.mgz
    "freesurfer_wm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Segmented white-matter volume.",
    },
    # mri/wmparc.mgz
    "freesurfer_wmparc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Aparc parcellation projected into subcortical white matter.",
    },
    # mri/wmparc_stats.mgz
    "freesurfer_wmparc_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "White matter parcellation statistics file.",
    },
    "freesurfer_BA_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Brodmann Area statistics files.",
    },
    "freesurfer_annot": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Surface annotation files.",
    },
    "freesurfer_aparc_a2009s_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Aparc a2009s parcellation statistics files.",
    },
    "freesurfer_aparc_aseg": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Aparc parcellation projected into aseg volume.",
    },
    "freesurfer_aparc_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Aparc parcellation statistics files.",
    },
    "freesurfer_area_pial": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Mean area of triangles each vertex on the pial surface is associated with.",
    },
    "freesurfer_avg_curv": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Average atlas curvature, sampled to subject.",
    },
    "freesurfer_curv": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Maps of surface curvature.",
    },
    "freesurfer_curv_pial": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Curvature of pial surface.",
    },
    "freesurfer_curv_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Curvature statistics files.",
    },
    "freesurfer_entorhinal_exvivo_stats": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Entorhinal exvivo statistics files.",
    },
    "freesurfer_graymid": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Graymid/midthickness surface meshes.",
    },
    "freesurfer_inflated": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Inflated surface meshes.",
    },
    "freesurfer_jacobian_white": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Distortion required to register to spherical atlas.",
    },
    "freesurfer_label": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Volume and surface label files.",
    },
    "freesurfer_pial": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Gray matter/pia mater surface meshes.",
    },
    "freesurfer_ribbon": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Volumetric maps of cortical ribbons.",
    },
    "freesurfer_smoothwm": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Smoothed original surface meshes.",
    },
    "freesurfer_sphere": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Spherical surface meshes.",
    },
    "freesurfer_sphere_reg": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Spherical registration file.",
    },
    "freesurfer_sulc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Surface maps of sulcal depth.",
    },
    "freesurfer_thickness": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Surface maps of cortical thickness.",
    },
    "freesurfer_volume": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Surface maps of cortical volume.",
    },
    "freesurfer_white": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "White/gray matter surface meshes.",
    },
}


# flake8: noqa: E501
