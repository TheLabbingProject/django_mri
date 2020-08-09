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
BET_CONFIGURATION = {"mask": True, "frac": 0.15}
MRCONVERT_CONFIGURATION = {}
DENOISE_CONFIGURATION = {}
DWIFSLPREPROC_CONFIGURATION = {
    "align_seepi": True,
    "rpe_pair": True,
    "eddy_oprions": " --slm=linear ",
}
DEGIBBS_CONFIGURATION = {}
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
# Generate dual-phase encoded image
CONVERT_MERGED_TO_MIF = {
    "source": MERGE_NODE,
    "source_port": "merged_file",
    "destination": MRCONVERT_NODE,
    "destination_port": "in_file",
}
PASS_MERGED_MIF_TO_DWIFSLPREPROC = {
    "source": MRCONVERT_NODE,
    "source_port": "out_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "se_epi",
}
PASS_MASK_TO_DENOISE = {
    "source": BET_NODE,
    "source_port": "mask_file",
    "destination": DENOISE_NODE,
    "destination_port": "mask",
}
DEGIBBSED_PIPE_MAIN = {
    "source": DWIFSLPREPROC_NODE,
    "source_port": "preprocessed_dwi",
    "destination": DEGIBBS_NODE,
    "destination_port": "in_file",
}

DEGIBBSED_PIPE_MASK = {
    "source": DWIFSLPREPROC_NODE,
    "source_port": "eddy_mask",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_mask",
}
