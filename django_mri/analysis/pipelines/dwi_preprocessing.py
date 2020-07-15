"""
Full DWI preprocessing pipeline.
"""

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
MEAN_CONFIGURATION = {"dimension": "T"}
BET_CONFIGURATION = {"mask": True}
MRCONVERT_CONFIGURATION = {}
DENOISE_CONFIGURATION = {}
DWIFSLPREPROC_CONFIGURATION = {"align_seepi": True, "rpe_pair": True}
DEGIBBS_CONFIGURATION = {}
BIAS_CORRECT_CONFIGURATION = {"use_ants": True}

