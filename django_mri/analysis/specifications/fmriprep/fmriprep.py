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
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
    FloatInputDefinition,
)
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    ListOutputDefinition,
)
from traits.trait_types import String


#: *fmriprep* input specification.
FMRIPREP_INPUT_SPECIFICATION = {
    "destination": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "run_method_input": True,
        "required": True,
        "description": "Path to output directory",
    },
    "analysis_level": {
        "type": StringInputDefinition,
        "choices": ["participant"],
        "required": True,
        "default": "participant",
        "description": "processing stage to be run, only “participant” in the case of fMRIPrep (see BIDS-Apps specification).",  # noqa: E501
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
    "task-id": {
        "type": StringInputDefinition,
        "description": "select a specific task to be processed",
    },
    "echo-idx": {
        "type": StringInputDefinition,
        "description": "select a specific echo to be processed in a multiecho series",
    },
    "bids-filter-file": {
        "type": FileInputDefinition,
        "description": "a JSON file describing custom BIDS input filters using PyBIDS.",
    },
    "anat-derivatives": {
        "type": DirectoryInputDefinition,
        "description": "Reuse the anatomical derivatives from another fMRIPrep run or calculated with an alternative processing tool (NOT RECOMMENDED).",
    },
    "bids-database-dir": {
        "type": DirectoryInputDefinition,
        "description": "Path to an existing PyBIDS database folder, for faster indexing (especially useful for large datasets).",
    },
    "nprocs": {
        "type": IntegerInputDefinition,
        "description": "maximum number of threads across all processes",
    },
    "omp-nthreads": {
        "type": IntegerInputDefinition,
        "description": "maximum number of threads per-process",
    },
    "mem": {
        "type": IntegerInputDefinition,
        "description": "upper bound memory limit for fMRIPrep processes",
    },
    "low-mem": {
        "type": BooleanInputDefinition,
        "description": "attempt to reduce memory usage (will increase disk usage in working directory)",
    },
    "use-plugin": {
        "type": FileInputDefinition,
        "description": "nipype plugin configuration file",
    },
    "anat-only": {
        "type": BooleanInputDefinition,
        "description": "run anatomical workflows only",
    },
    "boilerplate_only": {
        "type": BooleanInputDefinition,
        "description": "generate boilerplate only",
    },
    "md-only-boilerplate": {
        "type": BooleanInputDefinition,
        "description": "skip generation of HTML and LaTeX formatted citation with pandoc",
    },
    "error-on-aroma-warnings": {
        "type": BooleanInputDefinition,
        "description": "Raise an error if ICA_AROMA does not produce sensible output (e.g., if all the components are classified as signal or noise)",
    },
    ### Workflow configuration ###
    "ignore": {
        "type": ListInputDefinition,
        "choices": ["fieldmaps", "slicetiming", "sbref", "t2w", "flair"],
        "description": "ignore selected aspects of the input dataset to disable corresponding parts of the workflow (a space delimited list)",
    },
    "longitudinal": {
        "type": BooleanInputDefinition,
        "description": "treat dataset as longitudinal - may increase runtime",
    },
    "output-spaces": {
        "type": ListInputDefinition,
        "description": "Standard and non-standard spaces to resample anatomical and functional images to.",
    },
    "bold2t1w-init": {
        "type": StringInputDefinition,
        "choices": ["register", "header"],
        "default": "register",
    },
    "bold2t1w-dof": {
        "type": IntegerInputDefinition,
        "choices": [6, 9, 12],
        "description": "Degrees of freedom when registering BOLD to T1w images. 6 degrees (rotation and translation) are used by default.",
    },
    "force-bbr": {
        "type": BooleanInputDefinition,
        "description": "Always use boundary-based registration (no goodness-of-fit checks)",
    },
    "force-no-bbr": {
        "type": BooleanInputDefinition,
        "description": "Do not use boundary-based registration (no goodness-of-fit checks)",
    },
    "medial-surface-nan": {
        "type": BooleanInputDefinition,
        "description": "Replace medial wall values with NaNs on functional GIFTI files. Only performed for GIFTI files mapped to a freesurfer subject (fsaverage or fsnative).",
    },
    "dummy-scans": {
        "type": IntegerInputDefinition,
        "description": "Number of non steady state volumes.",
    },
    "random-seed": {
        "type": IntegerInputDefinition,
        "description": "Initialize the random seed for the workflow",
    },
    ### Specific options for running ICA_AROMA ###
    "use-aroma": {
        "type": BooleanInputDefinition,
        "description": "add ICA_AROMA to your preprocessing stream",
    },
    "aroma-melodic-dimensionality": {
        "type": IntegerInputDefinition,
        "description": "Exact or maximum number of MELODIC components to estimate (positive = exact, negative = maximum)",
    },
    ### Specific options for estimating confounds ###
    "return-all-components": {
        "type": BooleanInputDefinition,
        "description": "Include all components estimated in CompCor decomposition in the confounds file instead of only the components sufficient to explain 50 percent of BOLD variance in each CompCor mask",
    },
    "fd-spike-threshold": {
        "type": FloatInputDefinition,
        "description": "Threshold for flagging a frame as an outlier on the basis of framewise displacement",
    },
    "dvars-spike-threshold": {
        "type": FloatInputDefinition,
        "description": "Threshold for flagging a frame as an outlier on the basis of standardised DVARS",
    },
    ### Specific options for ANTs registrations ###
    "skull-strip-template": {
        "type": FileInputDefinition,
        "description": "select a template for skull-stripping with antsBrainExtraction",
    },
    "skull-strip-fixed-seed": {
        "type": BooleanInputDefinition,
        "description": "do not use a random seed for skull-stripping - will ensure run-to-run replicability when used with –omp-nthreads 1 and matching –random-seed <int>",
    },
    "skull-strip-t1w": {
        "type": StringInputDefinition,
        "choices": ["auto", "skip", "force"],
        "description": "determiner for T1-weighted skull stripping (‘force’ ensures skull stripping, ‘skip’ ignores skull stripping, and ‘auto’ applies brain extraction based on the outcome of a heuristic to check whether the brain is already masked).",
    },
    ### Specific options for handling fieldmaps ###
    "fmap-bspline": {
        "type": BooleanInputDefinition,
        "description": "fit a B-Spline field using least-squares (experimental)",
    },
    "fmap-no-demean": {
        "type": BooleanInputDefinition,
        "description": "do not remove median (within mask) from fieldmap",
    },
    ### Specific options for SyN distortion correction ###
    "use-syn-sdc": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL: Use fieldmap-free distortion correction",
    },
    "force-syn": {
        "type": BooleanInputDefinition,
        "description": "EXPERIMENTAL/TEMPORARY: Use SyN correction in addition to fieldmap correction, if available",
    },
    ### Specific options for FreeSurfer preprocessing ###
    "fs-license-file": {
        "type": FileInputDefinition,
        "description": "Path to FreeSurfer license key file.",
    },
    "fs-subjects-dir": {
        "type": DirectoryInputDefinition,
        "description": "Path to existing FreeSurfer subjects directory to reuse.",
    },
    ### Surface preprocessing options ###
    "no-submm-recon": {
        "type": BooleanInputDefinition,
        "description": "disable sub-millimeter (hires) reconstruction",
    },
    "cifti-output": {
        "type": StringInputDefinition,
        "choices": ["91k", "170k"],
        "description": "output preprocessed BOLD as a CIFTI dense timeseries. Optionally, the number of grayordinate can be specified (default is 91k, which equates to 2mm resolution)",
    },
    "fs-no-reconall": {
        "type": BooleanInputDefinition,
        "description": "disable FreeSurfer surface preprocessing.",
    },
    ### Other options ###
    "output-layout": {
        "type": StringInputDefinition,
        "choices": ["bids", "legacy"],
        "description": "Organization of outputs.",
    },
    "work-dir": {
        "type": DirectoryInputDefinition,
        "description": "path where intermediate results should be stored",
    },
    "clean-workdir": {
        "type": BooleanInputDefinition,
        "description": "Clears working directory of contents. Use of this flag is notrecommended when running concurrent processes of fMRIPrep.",
    },
    "resource-monitor": {
        "type": BooleanInputDefinition,
        "description": "enable Nipype’s resource monitoring to keep track of memory and CPU usage",
    },
    "reports-only": {
        "type": BooleanInputDefinition,
        "description": "only generate reports, don’t run workflows. This will only rerun report aggregation, not reportlet generation for specific nodes.",
    },
    "config-file": {
        "type": FileInputDefinition,
        "description": "Use pre-generated configuration file. Values in file will be overridden by command-line arguments.",
    },
    "write-graph": {
        "type": BooleanInputDefinition,
        "description": "Write workflow graph.",
    },
    "stop-on-first-crash": {
        "type": BooleanInputDefinition,
        "description": "Force stopping on first crash, even if a work directory was specified.",
    },
    "notrack": {
        "type": BooleanInputDefinition,
        "description": "Opt-out of sending tracking information of this run to the FMRIPREP developers.",
    },
    "debug": {
        "type": StringInputDefinition,
        "choices": ["compcor", "all"],
        "description": "Debug mode(s) to enable. ‘all’ is alias for all available modes.",
    },
    "sloppy": {
        "type": BooleanInputDefinition,
        "description": "Use low-quality tools for speed - TESTING ONLY",
    },
}
#: *fMRIprep* output specification.
FMRIPREP_OUTPUT_SPECIFICATION = {
    ### fmriprep
    ## native
    # anat/*desc-preproc_T1w.nii.gz
    "native_T1w": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical image in native space.",
    },
    # anat/*desc-brain_mask.nii.gz
    "native_brain_mask": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical brain mask in native space.",
    },
    # anat/*dseg.nii.gz
    "native_parcellation": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical brain parcellation in native space.",
    },
    # anat/*CSF_probseg.nii.gz
    "native_csf": {
        "type": FileOutputDefinition,
        "description": "CSF mask in native space.",
    },
    # anat/*GM_probseg.nii.gz
    "native_gm": {
        "type": FileOutputDefinition,
        "description": "GM mask in native space.",
    },
    # anat/*WM_probseg.nii.gz
    "native_wm": {
        "type": FileOutputDefinition,
        "description": "WM mask in native space.",
    },
    ## standard
    # anat/*desc-preproc_T1w.nii.gz
    "standard_T1w": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical image in standard space.",
    },
    # anat/*desc-brain_mask.nii.gz
    "standard_brain_mask": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical brain mask in standard space.",
    },
    # anat/*dseg.nii.gz
    "standard_parcellation": {
        "type": FileOutputDefinition,
        "description": "Preprocessed anatomical brain parcellation in standard space.",
    },
    # anat/*CSF_probseg.nii.gz
    "standard_csf": {
        "type": FileOutputDefinition,
        "description": "CSF mask in standard space.",
    },
    # anat/*GM_probseg.nii.gz
    "standard_gm": {
        "type": FileOutputDefinition,
        "description": "GM mask in standard space.",
    },
    # anat/*WM_probseg.nii.gz
    "standard_wm": {
        "type": FileOutputDefinition,
        "description": "WM mask in standard space.",
    },
    # anat/*from-T1wto-MNI..._mode-image_xfm.h5
    "native_to_mni_transform": {
        "type": FileOutputDefinition,
        "description": "Transformation file from native to standard space.",
    },
    # anat/*from-MNI...to-T1w_mode-image_xfm.h5
    "mni_to_native_transform": {
        "type": FileOutputDefinition,
        "description": "Transformation file from standard to native space.",
    },
    # anat/*from-fsnative...to-T1w_mode-image_xfm.txt
    "native_to_fsnative_transform": {
        "type": FileOutputDefinition,
        "description": "Transformation file from native to freesurfer's standard space.",
    },
    # anat/*from-fsnative...to-T1w_mode-image_xfm.txt
    "fsnative_to_native_transform": {
        "type": FileOutputDefinition,
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
    "native_boldref": {
        "type": FileOutputDefinition,
        "description": "Single volume BOLD reference in native space.",
    },
    # brain_mask
    "native_func_brain_mask": {
        "type": FileOutputDefinition,
        "description": "Functional image's brain mask in native space.",
    },
    # preproc_bold
    "native_preproc_bold": {
        "type": FileOutputDefinition,
        "description": "Preprocessed functional image in native space.",
    },
    # aparcaseg_dseg
    "native_aparc_bold": {
        "type": FileOutputDefinition,
        "description": "Aparc parcellation in functional image space.",
    },
    # aparcaseg_dseg
    "native_aseg_bold": {
        "type": FileOutputDefinition,
        "description": "Aseg parcellation in functional image space.",
    },
    # standard
    # boldref
    "standard_boldref": {
        "type": FileOutputDefinition,
        "description": "Single volume BOLD reference in standard space.",
    },
    # brain_mask
    "standard_func_brain_mask": {
        "type": FileOutputDefinition,
        "description": "Functional image's brain mask in standard space.",
    },
    # preproc_bold
    "standard_preproc_bold": {
        "type": FileOutputDefinition,
        "description": "Preprocessed functional image in standard space.",
    },
    # aparcaseg_dseg
    "standard_aparc_bold": {
        "type": FileOutputDefinition,
        "description": "Aparc parcellation in standard space.",
    },
    # aparcaseg_dseg
    "standard_aseg_bold": {
        "type": FileOutputDefinition,
        "description": "Aseg parcellation in standard space.",
    },
    ### Confounds ###
    "confounds_tsv": {
        "type": FileOutputDefinition,
        "description": "Extracted confounding time series in a .tsv format.",
    },
    "confounds_json": {
        "type": FileOutputDefinition,
        "description": "Extracted confounding time series in a .json format.",
    },
    # freesurfer/
    # mri/T1.mgz
    "freesurfer_T1": {
        "type": FileOutputDefinition,
        "description": "Intensity normalized whole-head volume.",
    },
    # mri/rawavg.mgz
    "freesurfer_rawavg": {
        "type": FileOutputDefinition,
        "description": "An average volume of the raw input data (if there is only one input volume, they will be identical). This volume is unconformed (i.e. to 256^3, 1mm isotropic)",  # noqa: E501
    },
    # mri/orig.mgz
    "freesurfer_orig": {
        "type": FileOutputDefinition,
        "description": "A conformed (i.e. to 256^3, 1mm isotropic) average volume of the raw input data.",
    },
    # mri/nu.mgz
    "freesurfer_nu": {
        "type": FileOutputDefinition,
        "description": "This is an intensity normalized volume generated after correcting for non-uniformity in conformed raw average (saved as 'mri/orig.mgz'). If there are any errors in later steps, it sometimes helps to check if the intensity values don't look normal in this file. If the values are too high, then scaling down the intensity a little bit and re-running recon-all usually corrects that error. In some cases, this scaling down can also be done for the orig.mgz volume.",  # noqa: E501
    },
    # mri/norm.mgz
    "freesurfer_norm": {
        "type": FileOutputDefinition,
        "description": "Normalized skull-stripped volume.",
    },
    # mri/aseg.mgz
    "freesurfer_aseg": {
        "type": FileOutputDefinition,
        "description": "Volumetric map of regions from automatic segmentation.",
    },
    # stats/aseg.stats
    "freesurfer_aseg_stats": {
        "type": FileOutputDefinition,
        "description": "Automated segmentation statistics file.",
    },
    # mri/brain.mgz
    "freesurfer_brain": {
        "type": FileOutputDefinition,
        "description": "Intensity normalized brain-only volume.",
    },
    # mri/brainmask.mgz
    "freesurfer_brainmask": {
        "type": FileOutputDefinition,
        "description": "Skull-stripped (brain-only) volume.",
    },
    # mri/filled.mgz
    "freesurfer_filled": {
        "type": FileOutputDefinition,
        "description": "Subcortical mass volume.",
    },
    # mri/wm.mgz
    "freesurfer_wm": {
        "type": FileOutputDefinition,
        "description": "Segmented white-matter volume.",
    },
    # mri/wmparc.mgz
    "freesurfer_wmparc": {
        "type": FileOutputDefinition,
        "description": "Aparc parcellation projected into subcortical white matter.",
    },
    # mri/wmparc_stats.mgz
    "freesurfer_wmparc_stats": {
        "type": FileOutputDefinition,
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
