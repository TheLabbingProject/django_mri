from django_mri.models.nifti import NIfTI


try:
    MNI = NIfTI.objects.get(path__contains="MNI152_T1_2mm_brain")
except NIfTI.DoesNotExist:
    raise NIfTI.DoesNotExist("Could not find MNI152_T1_2mm_brain in the database.")


BET_CONFIGURATION = {"robust": True}
REORIENT_CONFIGURATION = {}
ROBUSTFOV_CONFIGURATION = {}
FLIRT_CONFIGURATION = {"reference": MNI.id, "interp": "spline"}
FNIRT_CONFIGURATION = {"ref_file": MNI.id}

BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}
REORIENT_NODE = {
    "analysis_version": "fslreorient2std",
    "configuration": REORIENT_CONFIGURATION,
}
ROBUST_FOV_NODE = {
    "analysis_version": "robustfov",
    "configuration": ROBUSTFOV_CONFIGURATION,
}
FLIRT_NODE = {
    "analysis_version": "FLIRT",
    "configuration": {"reference": MNI.id, "interp": "spline"},
}

# Pipe configurations
BET_TO_REORIENT = {
    "source": BET_NODE,
    "source_port": "out_file",
    "destination": REORIENT_NODE,
    "destination_port": "in_file",
}
FNIRT_NODE = {
    "analysis_version": "FNIRT",
    "configuration": {"ref_file": MNI.id},
}

REORIENT_TO_FOV = {
    "source": REORIENT_NODE,
    "source_port": "out_file",
    "destination": ROBUST_FOV_NODE,
    "destination_port": "in_file",
}
FOV_TO_FLIRT = {
    "source": ROBUST_FOV_NODE,
    "source_port": "out_roi",
    "destination": FLIRT_NODE,
    "destination_port": "in_file",
}
FLIRT_TO_FNIRT = {
    "source": FLIRT_NODE,
    "source_port": "out_file",
    "destination": FNIRT_NODE,
    "destination_port": "in_file",
}

BASIC_FSL_PREPROCESSING = {
    "title": "Basic FSL Preprocessing",
    "description": "Basic MRI preprocessing pipeline using FSL.",
    "pipes": [BET_TO_REORIENT, REORIENT_TO_FOV, FOV_TO_FLIRT, FLIRT_TO_FNIRT],
}

pipeline_definitions = [BASIC_FSL_PREPROCESSING]
