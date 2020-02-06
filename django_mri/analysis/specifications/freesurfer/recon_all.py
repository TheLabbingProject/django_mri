from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    DirectoryInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)

from django_analyses.models.output.definitions import FileOutputDefinition

RECON_ALL_INPUT_SPECIFICATION = {
    "subject_id": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Subject ID to be searched for in the SUBJECTS_DIR path.",
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
        "description": "Directives control the execution of the various processing procedures carried out.",
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
        "description": "A list of T1 files to be processed, in either DICOM or NIfTI format.",
    },
    "T2_file": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Path to T2 image to be used for improved pial surface estimation (can be either a DICOM, MGH or NIFTI file)",
    },
    "use_T2": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Whether to use the provided T2 image to generate an improved pial surface estimation.",
    },
    "FLAIR_file": {
        "type": FileInputDefinition,
        "required": False,
        "description": "Path to FLAIR image to be used for improved pial surface estimation (can be either a DICOM, MGH or NIFTI file)",
    },
    "use_FLAIR": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Whether to use the provided FLAIR image to generate an improved pial surface estimation.",
    },
    "parallel": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Enable parallel execution.",
    },
    "openmp": {
        "type": IntegerInputDefinition,
        "required": False,
        "description": "Number of processes to run if parallel execution is enabled.",
    },
    "hires": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Conform to minimum voxel size (for voxels lesser than 1mm).",
    },
    "mprage": {
        "type": BooleanInputDefinition,
        "required": False,
        "description": "Assume scan parameters are MGH MPRAGE protocol, which produces darker grey matter.",
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
        "required": False,
        "description": "Path to subjects directory.",
    },
    "flags": {
        "type": ListInputDefinition,
        "element_type": "STR",
        "required": False,
        "description": "Additional parameters.",
    },
}
