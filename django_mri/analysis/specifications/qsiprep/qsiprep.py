"""
Input and output specification dictionaries for FreeSurfer's recon_all_ script.

.. _recon_all:
   https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all
"""

from django.conf import settings
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)
from traits.trait_types import Bool, String

#: *qsiprep* input specification.
QSIPREP_INPUT_SPECIFICATION = {
    "destination": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "required": True,
        "description": "Path to output directory",
    },
    "analysis_level": {
        "type": StringInputDefinition,
        "choices": ["participant"],
        "required": False,
        "default": "participant",
        "description": "processing stage to be run, only “participant” in the case of fMRIPrep (see BIDS-Apps specification).",  # noqa: E501
    },
    "output_resolution": {
        "type": FloatInputDefinition,
        "required": True,
        "description": "the isotropic voxel size in mm the data will be resampled to after preprocessing.",
    },
    ### Options to handle performance ###
    "skip_bids_validation": {
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
    "acquisition_type": {
        "type": StringInputDefinition,
        "description": "select a specific acquisition type to be processed",
    },
    "bids-filter-file": {
        "type": FileInputDefinition,
        "description": "a JSON file describing custom BIDS input filters using PyBIDS.",
    },
    "bids_database_dir": {
        "type": DirectoryInputDefinition,
        "description": "Path to an existing PyBIDS database folder, for faster indexing (especially useful for large datasets).",
    },
    "interactive_reports_only": {
        "type": BooleanInputDefinition,
        "description": "create interactive report json files on already preprocessed data.",
    },
    "recon_only": {
        "type": BooleanInputDefinition,
        "description": "run only reconstruction, assumes preprocessing has already completed.",
    },
    "recon_spec": {
        "type": FileInputDefinition,
        "description": "json file specifying a reconstruction pipeline to be run after preprocessing.",
    },
    "recon_input": {
        "type": StringInputDefinition,
        "description": "use this directory as inputs to qsirecon. This option skips qsiprep.",
    },
    "nthreads": {
        "type": IntegerInputDefinition,
        "description": "maximum number of threads across all processes.",
    },
    "omp_nthreads": {
        "type": IntegerInputDefinition,
        "description": "maximum number of threads per-process",
    },
    "mem_mb": {
        "type": IntegerInputDefinition,
        "description": "upper bound memory limit for fMRIPrep processes",
    },
    "low_mem": {
        "type": BooleanInputDefinition,
        "description": "attempt to reduce memory usage (will increase disk usage in working directory)",
    },
    "use_plugin": {
        "type": FileInputDefinition,
        "description": "nipype plugin configuration file",
    },
    "anat_only": {
        "type": BooleanInputDefinition,
        "description": "run anatomical workflows only",
    },
    "dwi_only": {
        "type": BooleanInputDefinition,
        "description": "ignore anatomical (T1w/T2w) data and process DWIs only",
    },
    "infant": {
        "type": BooleanInputDefinition,
        "description": "configure pipelines to process infant brains",
    },
    "boilerplate": {
        "type": BooleanInputDefinition,
        "description": "generate boilerplate only",
    },
    ### Workflow configuration ###
    "ignore": {
        "type": StringInputDefinition,
        "choices": ["fieldmaps", "sbref"],
        "description": "ignore selected aspects of the input dataset to disable corresponding parts of the workflow (a space delimited list)",
    },
    "longitudinal": {
        "type": BooleanInputDefinition,
        "description": "treat dataset as longitudinal _ may increase runtime",
    },
    "b0_threshold": {
        "type": FloatInputDefinition,
        "description": "any value in the .bval file less than this will be considered a b=0 image. Current default threshold = 100; this threshold can be lowered or increased. Note, setting this too high can result in inaccurate results.",
    },
    "dwi_denoise_window": {
        "type": IntegerInputDefinition,
        "description": "window size in voxels for image-based denoising.",
    },
    "denoise_method": {
        "type": StringInputDefinition,
        "choices": ["dwidenoise", "patch2self", "none"],
        "description": "Image-based denoising method. ",
    },
    "unringing_method": {
        "type": StringInputDefinition,
        "choices": ["none", "mrdegibbs"],
        "description": "Image-based Gibbs unringing method.",
    },
    "dwi_no_biascorr": {
        "type": BooleanInputDefinition,
        "description": "skip b0-based dwi spatial bias correction",
    },
    "no_b0_harmonization": {
        "type": BooleanInputDefinition,
        "description": "skip re-scaling dwi scans to have matching b=0 intensities",
    },
    "denoise_after_combining": {
        "type": BooleanInputDefinition,
        "description": "run dwidenoise after combining dwis. Requires --combine-all-dwis",
    },
    "separate_all_dwis": {
        "type": BooleanInputDefinition,
        "description": "don’t attempt to combine dwis from multiple runs. Each will be processed separately.",
    },
    "distortion_group_merge": {
        "type": StringInputDefinition,
        "choices": ["concat", "average", "none"],
        "description": "How to combine images across distorted groups.",
    },
    "write_local_bvecs": {
        "type": BooleanInputDefinition,
        "description": "write a series of voxelwise bvecs, relevant if writing preprocessed dwis to template space.",
    },
    "b0_to_t1w_transform": {
        "type": StringInputDefinition,
        "choices": ["Rigid", "Affine"],
        "description": "Degrees of freedom when registering b0 to T1w images. 6 degrees (rotation and translation) are used by default.",
    },
    "intramodal_template_iters": {
        "type": IntegerInputDefinition,
        "description": "Number of iterations for finding the midpoint image from the b0 templates from all groups.",
    },
    "intramodal_template_transform": {
        "type": StringInputDefinition,
        "choices": ["Rigid", "Affine", "BSplineSyN", "SyN"],
        "description": "Transformation used for building the intramodal template.",
    },
    # Motion correction and coregistration
    "b0_motion_corr_to": {
        "type": StringInputDefinition,
        "choices": ["iterative", "first"],
        "description": "align to the “first” b0 volume or do an “iterative” registration of all b0 images to their midpoint image.",
    },
    "hmc_transform": {
        "type": StringInputDefinition,
        "choices": ["Affine", "Rigid"],
        "description": "transformation to be optimized during head motion correction.",
    },
    "hmc_model": {
        "type": StringInputDefinition,
        "choices": ["3dSHORE", "eddy", "eddy"],
        "description": "model used to generate target images for hmc. If “none” the non-b0 images will be warped using the same transform as their nearest b0 image. If “3dSHORE”, SHORELine will be used. If “eddy_ingress”, the dwis are assumed to have been run through fsls eddy.",
    },
    "eddy_config": {
        "type": FileInputDefinition,
        "description": "path to a json file with settings for the call to eddy.",
    },
    "shoreline_iters": {
        "type": IntegerInputDefinition,
        "description": "number of SHORELine iterations.",
    },
    "impute_slice_threshold": {
        "type": IntegerInputDefinition,
        "description": "impute data in slices that are this many SDs from expected. If 0 (default), no slices will be imputed.",
    },
    "force_no_bbr": {
        "type": BooleanInputDefinition,
        "description": "Do not use boundary-based registration (no goodness-of-fit checks)",
    },
    "medial_surface_nan": {
        "type": BooleanInputDefinition,
        "description": "Replace medial wall values with NaNs on functional GIFTI files. Only performed for GIFTI files mapped to a freesurfer subject (fsaverage or fsnative).",
    },
    "dummy_scans": {
        "type": IntegerInputDefinition,
        "description": "Number of non steady state volumes.",
    },
    "random_seed": {
        "type": IntegerInputDefinition,
        "description": "Initialize the random seed for the workflow",
    },
    ### Specific options for ANTs registrations ###
    "skull_strip_template": {
        "type": StringInputDefinition,
        "choices": ["OASIS", "NKI"],
        "description": "select a template for skull-stripping with antsBrainExtraction",
    },
    "skull_strip_fixed_seed": {
        "type": BooleanInputDefinition,
        "description": "do not use a random seed for skull-stripping - will ensure run-to-run replicability when used with –omp-nthreads 1 and matching –random-seed <int>",
    },
    "skip_t1_based_spatial_normalization": {
        "type": BooleanInputDefinition,
        "description": "skip running the t1w-based normalization to template space.",
    },
    "skull_strip_t1w": {
        "type": StringInputDefinition,
        "choices": ["auto", "skip", "force"],
        "description": "determiner for T1_weighted skull stripping (‘force’ ensures skull stripping, ‘skip’ ignores skull stripping, and ‘auto’ applies brain extraction based on the outcome of a heuristic to check whether the brain is already masked).",
    },
    ### Specific options for handling fieldmaps ###
    "fmap_bspline": {
        "type": BooleanInputDefinition,
        "description": "fit a B-Spline field using least-squares (experimental)",
    },
    "fmap_no_demean": {
        "type": BooleanInputDefinition,
        "description": "do not remove median (within mask) from fieldmap",
    },
    ### Specific options for SyN distortion correction ###
    "use_syn_sdc": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL: Use fieldmap-free distortion correction",
    },
    "force_syn": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL/TEMPORARY: Use SyN correction in addition to fieldmap correction, if available",
    },
    ### Specific options for FreeSurfer preprocessing ###
    "fs_license_file": {
        "type": FileInputDefinition,
        "description": "Path to FreeSurfer license key file.",
    },
    "do_reconall": {
        "type": BooleanInputDefinition,
        "description": "Run the FreeSurfer recon-all pipeline",
    },
    ### Specific options for handling fieldmaps ###
    "prefer_dedicated_fmaps": {
        "type": BooleanInputDefinition,
        "description": "orces unwarping to use files from the fmap directory instead of using an RPEdir scan from the same session.",
    },
    "fmap_bspline": {
        "type": BooleanInputDefinition,
        "description": "fit a B-Spline field using least-squares (experimental)",
    },
    "fmap_no_demean": {
        "type": BooleanInputDefinition,
        "description": "do not remove median (within mask) from fieldmap.",
    },
    ### Specific options for SyN distortion correction ###
    "use_syn_sdc": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL: Use fieldmap-free distortion correction.",
    },
    "force_syn": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL/TEMPORARY: Use SyN correction in addition to fieldmap correction, if available.",
    },
    ### Other options ###
    "work_dir": {
        "type": DirectoryInputDefinition,
        "description": "path where intermediate results should be stored",
        "default": "/output/work",
    },
    "resource_monitor": {
        "type": BooleanInputDefinition,
        "description": "enable Nipype’s resource monitoring to keep track of memory and CPU usage",
    },
    "reports_only": {
        "type": BooleanInputDefinition,
        "description": "only generate reports, don’t run workflows. This will only rerun report aggregation, not reportlet generation for specific nodes.",
    },
    "write_graph": {
        "type": BooleanInputDefinition,
        "description": "Write workflow graph.",
    },
    "stop_on_first_crash": {
        "type": BooleanInputDefinition,
        "description": "Force stopping on first crash, even if a work directory was specified.",
    },
    "notrack": {
        "type": BooleanInputDefinition,
        "description": "Opt-out of sending tracking information of this run to the FMRIPREP developers.",
    },
    "sloppy": {
        "type": BooleanInputDefinition,
        "description": "Use low-quality tools for speed - TESTING ONLY",
    },
}
#: *QSIprep* output specification.
QSIPREP_OUTPUT_SPECIFICATION = {
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
    ## functionals
    # native
    # boldref
    "native_dwiref": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Single volume DWI reference in native space.",
    },
    # brain_mask
    "native_dwi_brain_mask": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Diffusion image's brain mask in native space.",
    },
    # preproc_bold
    "native_preproc_dwi": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed DWI image in native space.",
    },
    "native_preproc_bvec": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed DWI image's corresponding bvec file.",
    },
    "native_preproc_bval": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed DWI image's corresponding bval file.",
    },
    "native_preproc_mrtrix_grad": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessed DWI image's corresponding gradient file.",
    },
    "native_eddy_cnr": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Eddy's CNR in native space.",
    },
    "native_dwi_qc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "DWI's QC json file.",
    },
    "native_dwi_sliceqc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "DWI's SliceQC json file.",
    },
    "native_dwi_imageqc": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "DWI's ImageQC csv file.",
    },
    "confounds_tsv": {
        "type": ListOutputDefinition,
        "element_type": "FIL",
        "description": "Preprocessing's confounds tsv file.",
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
