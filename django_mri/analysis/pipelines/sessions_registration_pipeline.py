FIRST_FLIRT_1_CONFIGURATION = {"cost": "mutualinfo"}
FIRST_FLIRT_2_CONFIGURATION = {"cost": "mutualinfo"}
MERGE_CONFIGURATION = {"dimension": "t"}

MEAN_CONFIGURATION = {"dimension": "T"}

SECOND_FLIRT_CONFIGURATION = {}

SECOND_FNIRT_CONFIGURATION = {}

THIRD_FLIRT_1_CONFIGURATION = {"apply_xfm":True}
THIRD_FLIRT_2_CONFIGURATION = {"apply_xfm":True}

THIRD_FNIRT_1_CONFIGURATION = {}
THIRD_FNIRT_2_CONFIGURATION = {}


FIRST_FLIRT_1_NODE = {
    "analysis_version": "FLIRT",
    "configuration": FIRST_FLIRT_1_CONFIGURATION,
}
FIRST_FLIRT_2_NODE = {
    "analysis_version": "FLIRT",
    "configuration": FIRST_FLIRT_2_CONFIGURATION,
}
MERGE_NODE = {
    "analysis_version": "fslmerge",
    "configuration": MERGE_CONFIGURATION,
}
MEAN_NODE = {
    "analysis_version": "mean_image",
    "configuration": MEAN_CONFIGURATION,
}
SECOND_FLIRT_NODE = {
    "analysis_version": "FLIRT",
    "configuration": SECOND_FLIRT_CONFIGURATION,
}
SECOND_FNIRT_NODE = {
    "analysis_version": "FNIRT",
    "configuration": SECOND_FNIRT_CONFIGURATION,
}
THIRD_FLIRT_1_NODE = {
    "analysis_version": "FLIRT",
    "configuration": THIRD_FLIRT_1_CONFIGURATION,
}
THIRD_FLIRT_2_NODE = {
    "analysis_version": "FLIRT",
    "configuration": THIRD_FLIRT_2_CONFIGURATION,
}
THIRD_FNIRT_1_NODE = = {
    "analysis_version": "FNIRT",
    "configuration": THIRD_FNIRT_1_CONFIGURATION,
}
THIRD_FNIRT_2_NODE = = {
    "analysis_version": "FNIRT",
    "configuration": THIRD_FNIRT_2_CONFIGURATION,
}

FLIRT_1_TO_MERGE = {
    "source": FIRST_FLIRT_1_NODE,
    "source_port": "out_file",
    "destination": MERGE_NODE,
    "destination_port": "in_files",
}
FLIRT_2_TO_MERGE = {
    "source": FIRST_FLIRT_2_NODE,
    "source_port": "out_file",
    "destination": MERGE_NODE,
    "destination_port": "in_files",
}
MERGE_TO_MEAN = {
    "source": MERGE_NODE,
    "source_port": "merged_file",
    "destination": MEAN_NODE,
    "destination_port": "in_file",
}
MEAN_TO_FLIRT = {
    "source": MEAN_NODE,
    "source_port": "out_file",
    "destination": SECOND_FLIRT_NODE,
    "destination_port": "reference",
}
MEAN_TO_FNIRT = {
    "source": MEAN_NODE,
    "source_port": "out_file",
    "destination": SECOND_FNIRT_NODE,
    "destination_port": "ref_file",
}
FLIRT_AFF_TO_FNIRT = {
    "source": SECOND_FLIRT_NODE,
    "source_port": "out_matrix_file",
    "destination": SECOND_FNIRT_NODE,
    "destination_port": "affine_file",
},
FLIRT_TO_TEMP_1 = {
    "source": FIRST_FLIRT_1_NODE,
    "source_port": "out_file",
    "destination": THIRD_FLIRT_1_NODE,
    "destination_port": "in_file",
},
FLIRT_TO_TEMP_1_AFF = {
    "source": SECOND_FLIRT_NODE,
    "source_port": "out_matrix_file",
    "destination": THIRD_FLIRT_1_NODE,
    "destination_port": "in_matrix_file",
},
FLIRT_TO_TEMP_2 = {
    "source": FIRST_FLIRT_2_NODE,
    "source_port": "out_file",
    "destination": THIRD_FLIRT_2_NODE,
    "destination_port": "in_file",
},
FLIRT_TO_TEMP_2_AFF = {
    "source": SECOND_FLIRT_NODE,
    "source_port": "out_matrix_file",
    "destination": THIRD_FLIRT_2_NODE,
    "destination_port": "in_matrix_file",
},

