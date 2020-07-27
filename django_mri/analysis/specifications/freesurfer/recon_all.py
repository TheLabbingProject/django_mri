"""
Input and output specification dictionaries for FreeSurfer's recon_all_ script.

.. _recon_all:
   https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all
"""

from django.conf import settings
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    DirectoryInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition


#: *recon_all* input specification.
RECON_ALL_INPUT_SPECIFICATION = {
    "subject_id": {
        "type": StringInputDefinition,
        "dynamic_default": "{run_id}",
        "required": True,
        "description": "Subject ID to be searched for in the SUBJECTS_DIR path.",  # noqa: E501
        "is_configuration": False,
    },
    "directive": {
        "type": StringInputDefinition,
        "choices": [
            "all",
            "autorecon1",
            # autorecon2 variants
            "autorecon2",
            "autorecon2-volonly",
            "autorecon2-perhemi",
            "autorecon2-inflate1",
            "autorecon2-cp",
            "autorecon2-wm",
            # autorecon3 variants
            "autorecon3",
            "autorecon3-T2pial",
            # Mix of autorecon2 and autorecon3 steps
            "autorecon-pial",
            "autorecon-hemi",
            # Not "multi-stage flags"
            "localGI",
            "qcache",
        ],
        "default": "all",
        "description": "Directives control the execution of the various processing procedures carried out.",  # noqa: E501
    },
    "hemi": {
        "type": StringInputDefinition,
        "choices": ["lh", "rh"],
        "required": False,
        "description": "Choose to run only for a particular hemisphere.",
    },
    "T1_files": {
        "type": ListInputDefinition,
        "element_type": "FIL",
        "required": False,
        "description": "A list of T1 files to be processed, in either DICOM or NIfTI format.",  # noqa: E501
    },
    "T2_file": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Path to T2 image to be used for improved pial surface estimation (can be either a DICOM, MGH or NIFTI file)",  # noqa: E501
    },
    "use_T2": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Whether to use the provided T2 image to generate an improved pial surface estimation.",  # noqa: E501
    },
    "FLAIR_file": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Path to FLAIR image to be used for improved pial surface estimation (can be either a DICOM, MGH or NIFTI file)",  # noqa: E501
    },
    "use_FLAIR": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Whether to use the provided FLAIR image to generate an improved pial surface estimation.",  # noqa: E501
    },
    "parallel": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Enable parallel execution.",
    },
    "openmp": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of processes to run if parallel execution is enabled.",  # noqa: E501
    },
    "hires": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Conform to minimum voxel size (for voxels lesser than 1mm).",  # noqa: E501
    },
    "mprage": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Assume scan parameters are MGH MPRAGE protocol, which produces darker grey matter.",  # noqa: E501
    },
    "big_ventricles": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "To be used for subjects with enlarged ventricles.",
    },
    "brainstem": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Segment brainstem structures.",
    },
    "hippocampal_subfields_T1": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Segment hippocampal subfields using the T1 image.",
    },
    "expert": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Set parameters using an expert file.",
    },
    "xopts": {
        "type": StringInputDefinition,
        "choices": ["use", "clean", "overwrite"],
        "required": False,
        "description": "Use, clean, or overwrite the existing experts file.",
    },
    "subjects_dir": {
        "type": DirectoryInputDefinition,
        "default": settings.ANALYSIS_BASE_PATH,
        "required": True,
        "description": "Path to subjects directory.",
    },
    "flags": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "required": False,
        "description": "Additional parameters.",
    },
    # Expert options
    "talairach": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to talairach commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_normalize": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_normalize commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_watershed": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_watershed commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_em_register": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_em_register commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_ca_normalize": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_ca_normalize commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_ca_register": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_ca_register commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_remove_neck": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_remove_neck commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_ca_label": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_ca_label commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_segstats": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_segstats commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_mask": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_mask commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_segment": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_segment commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_edit_wm_with_aseg": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_edit_wm_with_aseg commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_pretess": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_pretess commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_fill": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_fill commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_tessellate": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_tessellate commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_smooth": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_smooth commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_inflate": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_inflate commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_sphere": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_sphere commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_fix_topology": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_fix_topology commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_make_surfaces": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_make_surfaces commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_surf2vol": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_surf2vol commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_register": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_register commands.",
        # This should be mutually exclusive with "expert"
    },
    "mrisp_paint": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mrisp_paint commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_ca_label": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_ca_label commands.",
        # This should be mutually exclusive with "expert"
    },
    "mris_anatomical_stats": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mris_anatomical_stats commands.",
        # This should be mutually exclusive with "expert"
    },
    "mri_aparc2aseg": {
        "type": StringInputDefinition,
        "required": False,
        "description": "Flags to pass to mri_aparc2aseg commands.",
        # This should be mutually exclusive with "expert"
    },
}

#: *recon_all* output specification.
RECON_ALL_OUTPUT_SPECIFICATION = {
    # mri/T1.mgz
    "T1": {"type": FileOutputDefinition, "description": ""},
    # mri/rawavg.mgz
    "rawavg": {
        "type": FileOutputDefinition,
        "description": "An average volume of the raw input data (if there is only one input volume, they will be identical). This volume is unconformed (i.e. to 256^3, 1mm isotropic)",  # noqa: E501
    },
    # mri/orig.mgz
    "orig": {
        "type": FileOutputDefinition,
        "description": "A conformed (i.e. to 256^3, 1mm isotropic) average volume of the raw input data.",  # noqa: E501
    },
    # mri/nu.mgz
    "nu": {
        "type": FileOutputDefinition,
        "description": "This is an intensity normalized volume generated after correcting for non-uniformity in conformed raw average (saved as 'mri/orig.mgz'). If there are any errors in later steps, it sometimes helps to check if the intensity values don't look normal in this file. If the values are too high, then scaling down the intensity a little bit and re-running recon-all usually corrects that error. In some cases, this scaling down can also be done for the orig.mgz volume.",  # noqa: E501
    },
    # mri/norm.mgz
    "norm": {"type": FileOutputDefinition, "description": ""},
    # mri/aseg.mgz
    "aseg": {"type": FileOutputDefinition, "description": ""},
    # stats/aseg.stats
    "aseg_stats": {"type": FileOutputDefinition, "description": ""},
    # mri/brain.mgz
    "brain": {"type": FileOutputDefinition, "description": ""},
    # mri/brainmask.mgz
    "brainmask": {"type": FileOutputDefinition, "description": ""},
    # mri/filled.mgz
    "filled": {"type": FileOutputDefinition, "description": ""},
    # mri/wm.mgz
    "wm": {"type": FileOutputDefinition, "description": ""},
    # mri/wmparc.mgz
    "wmparc": {"type": FileOutputDefinition, "description": ""},
    # mri/wmparc_stats.mgz
    "wmparc_stats": {"type": FileOutputDefinition, "description": ""},
}
