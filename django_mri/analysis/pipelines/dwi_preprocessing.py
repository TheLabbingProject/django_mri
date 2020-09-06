"""
Full DWI preprocessing pipeline.

Steps:

    - Extract b0 from AP
    - Merge AP_b0 and PA
    - Create brain mask
    - Convert to mif (merged, AP)
    - Denoise initial AP
    - *dwifslpreproc* AP merged
    - Gibbs correction
    - Bias correction

User inputs:

    - *fslroi* node: in_file [AP]
    - *fslmerge* node: in_files [PA]
    - mrconvert_1 --> AP: in_bvec [bvec]
    - mrconvert_1 --> AP: in_bval [bval]

"""

# Configrations

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
FLIRT_CONFIGURATION = {"cost": "mutualinfo", "dof": 6}
BET_CONFIGURATION = {"mask": True, "robust": True}
MRCONVERT_CONFIGURATION = {}
DENOISE_CONFIGURATION = {}
DWIFSLPREPROC_CONFIGURATION = {
    "align_seepi": True,
    "rpe_pair": True,
    "eddy_options": '" --slm=linear"',
}
DEGIBBS_CONFIGURATION = {}
# BIAS_CORRECT_CONFIGURATION = {"use_ants": True}
BIAS_CORRECT_CONFIGURATION = {"use_ants": True}

# Nodes
FSLROI_NODE = {
    "analysis_version": "fslroi",
    "configuration": FSLROI_CONFIGURATION,
}
MERGE_NODE = {
    "analysis_version": "fslmerge",
    "configuration": MERGE_CONFIGURATION,
}
FLIRT_NODE = {
    "analysis_version": "FLIRT",
    "configuration": FLIRT_CONFIGURATION,
}
BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}
MRCONVERT_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_CONFIGURATION,
}
DENOISE_NODE = {
    "analysis_version": "denoise",
    "configuration": DENOISE_CONFIGURATION,
}
DWIFSLPREPROC_NODE = {
    "analysis_version": "dwifslpreproc",
    "configuration": DWIFSLPREPROC_CONFIGURATION,
}
DEGIBBS_NODE = {
    "analysis_version": "degibbs",
    "configuration": DEGIBBS_CONFIGURATION,
}
BIAS_CORRECT_NODE = {
    "analysis_version": "bias_correct",
    "configuration": BIAS_CORRECT_CONFIGURATION,
}


# Pipes

# Extract first, B0 volume
FIRST_AP_VOLUME_TO_MERGE = {
    "source": FSLROI_NODE,
    "source_port": "roi_file",
    "destination": MERGE_NODE,
    "destination_port": "in_files",
}
# FIRST_AP_TO_BET = {
#     "source": FSLROI_NODE,
#     "source_port": "roi_file",
#     "destination": BET_NODE,
#     "destination_port": "in_file",
# }
FIRST_AP_TO_FLIRT = {
    "source": FSLROI_NODE,
    "source_port": "roi_file",
    "destination": FLIRT_NODE,
    "destination_port": "reference",
}
FLIRT_TO_BET = {
    "source": FLIRT_NODE,
    "source_port": "out_file",
    "destination": BET_NODE,
    "destination_port": "in_file",
}
MASK_TO_DENOISE = {
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": DENOISE_NODE,
    "destination_port": "mask",
}
MERGED_TO_DWIFSLPREPROC = {
    "source": MERGE_NODE,
    "source_port": "merged_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "se_epi",
}
DENOISED_TO_DWIFSLPREPROC = {
    "source": DENOISE_NODE,
    "source_port": "out_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "scan",
}
MASK_TO_DWIFSLPREPROC = {
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "eddy_mask",
}
PREPROCESSED_TO_DEGIBBS = {
    "source": DWIFSLPREPROC_NODE,
    "source_port": "preprocessed_dwi",
    "destination": DEGIBBS_NODE,
    "destination_port": "in_file",
}
DEGIBBS_TO_BIAS_CORRECT = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_file",
}
MASK_TO_BIAS_CORRECT = {
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_mask",
}
DWI_PREPROCESSING_PIPELINE = {
    "title": "Basic DWI Preprocessing",
    "description": "Basic DWI preprocessing pipeline using FSL and Mrtrix3.",
    "pipes": [
        FIRST_AP_VOLUME_TO_MERGE,
        FIRST_AP_TO_FLIRT,
        FLIRT_TO_BET,
        MASK_TO_DENOISE,
        MERGED_TO_DWIFSLPREPROC,
        DENOISED_TO_DWIFSLPREPROC,
        MASK_TO_DWIFSLPREPROC,
        PREPROCESSED_TO_DEGIBBS,
        DEGIBBS_TO_BIAS_CORRECT,
        MASK_TO_BIAS_CORRECT,
    ],
}
