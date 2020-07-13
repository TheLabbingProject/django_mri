# Node configurations

FSLROI_CONFIGURATION = {
    "t_min": 0,
    "t_size": 1,
    "x_min": 0,
    "x_size": -1,
    "y_min": 0,
    "y_size": -1,
    "z_min": 0,
    "z_size": -1,
}
MERGE_CONFIGURATION = {"dimension": "t"}
TOPUP_CONFIGURATION = {}
MATHS_CONFIGURATION = {"operand_value": 6.28, "operation": "mul"}
MEAN_CONFIGURATION = {"dimension": "t"}
BET_CONFIGURATION = {}


# Node creation

FSLROI_NODE = {
    "analysis_version": "fslroi",
    "configuration": FSLROI_CONFIGURATION,
}
MERGE_NODE = {
    "analysis_version": "fslmerge",
    "configuration": MERGE_CONFIGURATION,
}
TOPUP_NODE = {
    "analysis_version": "topup",
    "configuration": TOPUP_CONFIGURATION,
}
BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}
MATHS_NODE = {
    "analysis_version": "binary_maths",
    "configuration": MATHS_CONFIGURATION,
}
MEAN_NODE = {
    "analysis_version": "mean_image",
    "configuration": MEAN_CONFIGURATION,
}

# Pipe creation

EXTRACT_VOLUME = {
    "source": FSLROI_NODE,
    "source_port": "roi_file",
    "destination": MERGE_NODE,
    "destination_port": "in_files",
}
MERGE_PHASEDIFF = {
    "source": MERGE_NODE,
    "source_port": "merged_file",
    "destination": TOPUP_NODE,
    "destination_port": "in_file",
}
CORRECT_FIELD = {
    "source": TOPUP_NODE,
    "source_port": "out_corrected",
    "destination": MEAN_NODE,
    "destination_port": "in_file",
}
RADIANS_PIPE = {
    "source": TOPUP_NODE,
    "source_port": "out_field",
    "destination": MATHS_NODE,
    "destination_port": "in_file",
}
BRAIN_EXTRACT = {
    "source": MEAN_NODE,
    "source_port": "out_file",
    "destination": BET_NODE,
    "destination_port": "in_file",
}


# Pipeline creation

FIELDMAP_CORRECTION = {
    "title": "Field-map correction",
    "description": "Field-map correction using FSL.",
    "pipes": [
        EXTRACT_VOLUME,
        MERGE_PHASEDIFF,
        CORRECT_FIELD,
        RADIANS_PIPE,
        BRAIN_EXTRACT,
    ],
}
