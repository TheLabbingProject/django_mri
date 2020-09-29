"""
Full DWI preprocessing pipeline.

steps:
"""

"""
- MRCONVERT #0 Importing DWI data into temporary directory
- MRCONVERT #1 Importing fmap data into temporary directory
- MRCONVERT #2 Separating fmap image from concatenated series
- MRCONVERT #3 Separating DWI images from concatenated series
"""
MRCONVERT_CONFIGURATION = {}
MRCONVERT_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_CONFIGURATION,
}

"""
- Concatenating DWI and fmap data for combined pre-processing
"""
MRCAT_CONFIGURATION = {"axis": 3}
MRCAT_NODE = {
    "analysis_version": "mrcat",
    "configuration": MRCAT_CONFIGURATION,
}

"""
- Performing MP-PCA denoising of DWI and fmap data
"""
DENOISE_CONFIGURATION = {}
DENOISE_NODE = {
    "analysis_version": "denoise",
    "configuration": DENOISE_CONFIGURATION,
}

"""
- Performing Gibbs ringing removal for DWI and fmap data
"""
DEGIBBS_CONFIGURATION = {"nshifts": 50}
DEGIBBS_NODE = {
    "analysis_version": "degibbs",
    "configuration": DEGIBBS_CONFIGURATION,
}

DWIGRADCHECK_CONFIGURATION = {}
DWIGRADCHECK_NODE = {
    "analysis_version": "dwigradcheck",
    "configuration": DWIGRADCHECK_CONFIGURATION,
}
"""
- Performing various geometric corrections of DWIs
"""
DWIFSLPREPROC_CONFIGURATION = {
    "align_seepi": True,
    "rpe_header": True,
    "eddy_options": '" --slm=linear"',
}
DWIFSLPREPROC_NODE = {
    "analysis_version": "dwifslpreproc",
    "configuration": DWIFSLPREPROC_CONFIGURATION,
}
"""
- Performing initial B1 bias field correction of DWIs
"""
BIAS_CORRECT_CONFIGURATION = {"use_ants": True}  ### FIX ANTS ISSUE!
BIAS_CORRECT_NODE = {
    "analysis_version": "bias_correct",
    "configuration": BIAS_CORRECT_CONFIGURATION,
}
# Pipes
MIF_FMAP_TO_CAT = {
    "source": MRCONVERT_NODE,
    "source_port": "out_file",
    "source_run_index":1,
    "destination": MRCAT_NODE,
    "destination_port": "in_files",
    "index":0,
}
MIF_DWI_TO_CAT = {
    "source": MRCONVERT_NODE,
    "source_port": "out_file",
    "source_run_index":0,
    "destination": MRCAT_NODE,
    "destination_port": "in_files",
    "index":1,
}
CAT_TO_DENOISE = {
    "source": MRCAT_NODE,
    "source_port": "out_file",
    "destination": DENOISE_NODE,
    "destination_port": "in_file",
}
DENOISE_TO_DEGIBBS = {
    "source": DENOISE_NODE,
    "source_port": "out_file",
    "destination": DEGIBBS_NODE,
    "destination_port": "in_file",
}
DEGIBBS_TO_SEP_1 = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": MRCONVERT_NODE,
    "destination_run_index":2,
    "destination_port": "in_file",
}
DEGIBBS_TO_SEP_2 = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": MRCONVERT_NODE,
    "destination_run_index":3,
    "destination_port": "in_file",
}
SEPERATE_TO_DWIGRADCHECK = {
    "source": MRCONVERT_NODE,
    "source_run_index":3,
    "source_port": "out_file",
    "destination": DWIGRADCHECK_NODE,
    "destination_port": "in_file",
}
FMAP_TO_DWIFSLPREPROC = {
    "source": MRCONVERT_NODE,
    "source_run_index":2,
    "source_port": "out_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "se_epi",
}
BVEC_TO_DWIFSLPREPROC = {
    "source": DWIGRADCHECK_NODE,
    "source_port": "grad_fsl_bvec",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "fslgrad",
}
BVAL_TO_DWIFSLPREPROC = {
    "source": DWIGRADCHECK_NODE,
    "source_port": "grad_fsl_bval",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "fslgrad",
}
DWI_TO_DWIFSLPREPROC = {
    "source": MRCONVERT_NODE,
    "source_run_index":3,
    "source_port": "out_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "scan",
}
PREPROCESSED_TO_BIAS_CORRECT = {
    "source": DWIFSLPREPROC_NODE,
    "source_port": "preprocessed_dwi",
    "destination": BIAS_CORRECT_NODE,
    "destination_port": "in_file",
}

DWI_PREPROCESSING_PIPELINE = {
    "title": "Basic and robust DWI Preprocessing",
    "description": "Basic DWI preprocessing pipeline using FSL and Mrtrix3.",
    "pipes": [
        MIF_FMAP_TO_CAT,
        MIF_DWI_TO_CAT,
        CAT_TO_DENOISE,
        DENOISE_TO_DEGIBBS,
        DEGIBBS_TO_SEP_1,
        DEGIBBS_TO_SEP_2,
        SEPERATE_TO_DWIGRADCHECK,
        FMAP_TO_DWIFSLPREPROC,
        BVEC_TO_DWIFSLPREPROC,
        BVAL_TO_DWIFSLPREPROC,
        DWI_TO_DWIFSLPREPROC,
        PREPROCESSED_TO_BIAS_CORRECT,
    ],
}
