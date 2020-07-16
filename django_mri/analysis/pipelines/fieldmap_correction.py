"""
Field-map correction for EPI scans using FSL.
"""


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
MEAN_CONFIGURATION = {"dimension": "T"}
MATHS_CONFIGURATION = {"operand_value": 6.28, "operation": "mul"}
BET_CONFIGURATION = {"mask": True}
EDDY_CONFIGURATION = {}
DENOISE_CONFIGURATION = {}
DEGIBBS_CONFIGURATION = {}
BIAS_CORRECT_CONFIGURATION = {"use_ants": True}
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
MEAN_NODE = {
    "analysis_version": "mean_image",
    "configuration": MEAN_CONFIGURATION,
}
MATHS_NODE = {
    "analysis_version": "binary_maths",
    "configuration": MATHS_CONFIGURATION,
}
BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}
EDDY_NODE = {"analysis_version": "eddy", "configuration": EDDY_CONFIGURATION}
DENOISE_NODE = {"analysis_version": "denoise", "configuration": DENOISE_CONFIGURATION}
DEGIBBS_NODE = {"analysis_version": "degibbs", "configuration": DEGIBBS_CONFIGURATION}
BIAS_CORRECT_NODE = {
    "analysis_version": "bias_correct",
    "configuration": BIAS_CORRECT_CONFIGURATION,
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
PERFORM_TOPUP = {
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
DENOISE_EPI = {  ############## multiple inputs from nodes \ user - ask Zvi #############
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": DENOISE_NODE,
    "destination_port": "mask",
}
############## Generate index.txt ##############
############## User should insert .bvec and .bval as inputs - we shpuld consider automating this ##############

EDDY_CORRECT = {
    "source": TOPUP_NODE,
    "source_port": "out_fieldcoef",
    "destination": EDDY_NODE,
    "destination_port": "in_topup_fieldcoef",
}
EDDY_CORRECT = {
    "source": TOPUP_NODE,
    "source_port": "out_movpar",
    "destination": EDDY_NODE,
    "destination_port": "in_topup_movpar",
}

EDDY_CORRECT = {
    "source": TOPUP_NODE,
    "source_port": "out_enc_file",
    "destination": EDDY_NODE,
    "destination_port": "in_acqp",
}
EDDY_CORRECT = {
    "source": BRAIN_EXTRACT,
    "source_port": "mask_file",
    "destination": EDDY_NODE,
    "destination_port": "in_mask",
}


CORRET_GIBBS = {
    "source": DENOISE_NODE,
    "source_port": "out_file",
    "destination": DEGIBBS_NODE,
    "destination_port": "in_file",
}
BIAS_CORRECT = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_file",
}
BIAS_CORRECT = {
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_mask",
}
# Pipeline creation

FIELDMAP_CORRECTION = {
    "title": "Field-map correction",
    "description": "Field-map correction using FSL.",
    "pipes": [
        EXTRACT_VOLUME,
        MERGE_PHASEDIFF,
        PERFORM_TOPUP,
        RADIANS_PIPE,
        BRAIN_EXTRACT,
        EDDY_CORRECT,
        DENOISE_CONFIGURATION,
        CORRET_GIBBS,
        BIAS_CORRECT,
    ],
}
