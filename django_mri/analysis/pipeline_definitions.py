from django_mri.models.nifti import NIfTI


try:
    MNI = NIfTI.objects.get(path__contains="MNI152_T1_2mm_brain")
except NIfTI.DoesNotExist:
    raise NIfTI.DoesNotExist("Could not find MNI152_T1_2mm_brain in the database.")


BASIC_FSL_PREPROCESSING = {
    "title": "Basic FSL Preprocessing",
    "description": "Basic MRI preprocessing pipeline using FSL.",
    "pipes": [
        {
            "source": {"analysis_version": "BET", "configuration": {"robust": True}},
            "source_port": "out_file",
            "destination": {"analysis_version": "fslreorient2std", "configuration": {}},
            "destination_port": "in_file",
        },
        {
            "source": {"analysis_version": "fslreorient2std", "configuration": {}},
            "source_port": "out_file",
            "destination": {"analysis_version": "robustfov", "configuration": {}},
            "destination_port": "in_file",
        },
        {
            "source": {"analysis_version": "robustfov", "configuration": {}},
            "source_port": "out_roi",
            "destination": {
                "analysis_version": "FLIRT",
                "configuration": {"reference": MNI.id, "interp": "spline"},
            },
            "destination_port": "in_file",
        },
        {
            "source": {
                "analysis_version": "FLIRT",
                "configuration": {"reference": MNI.id, "interp": "spline"},
            },
            "source_port": "out_file",
            "destination": {
                "analysis_version": "FNIRT",
                "configuration": {"ref_file": MNI.id},
            },
            "destination_port": "in_file",
        },
    ],
}

pipeline_definitions = [BASIC_FSL_PREPROCESSING]
