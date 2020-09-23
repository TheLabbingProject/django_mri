"""
Full DWI preprocessing pipeline.

steps:
"""

"""
- Importing DWI data into temporary directory
"""
MRCONVERT_DWI_CONFIGURATION = {}
MRCONVERT_DWI_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_DWI_CONFIGURATION,
}

"""
- Importing fmap data into temporary directory
"""
MRCONVERT_FMAP_CONFIGURATION = {}
MRCONVERT_FMAP_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_FMAP_CONFIGURATION,
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

"""
- Separating DWIs and fmap images from concatenated series
"""
MRCONVERT_SEPERATE_1_CONFIGURATION = {"coord": "3 0:0"}
MRCONVERT_SEPERATE_1_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_SEPERATE_1_CONFIGURATION,
}
MRCONVERT_SEPERATE_2_CONFIGURATION = {"coord": "3 1:88"}
MRCONVERT_SEPERATE_2_NODE = {
    "analysis_version": "mrconvert",
    "configuration": MRCONVERT_SEPERATE_2_CONFIGURATION,
}  #### Ask Zvi if I can get information regarding the size of the image - need to extract volumes 1:end

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
MIF_DWI_TO_CAT = {
    "source": MRCONVERT_DWI_NODE,
    "source_port": "out_file",
    "destination": MRCAT_NODE,
    "destination_port": "in_files",
}
MIF_FMAP_TO_CAT = {
    "source": MRCONVERT_FMAP_NODE,
    "source_port": "out_file",
    "destination": MRCAT_NODE,
    "destination_port": "in_files",
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
DEGIBBS_TO_SEP = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": MRCONVERT_SEPERATE_1_NODE,
    "destination_port": "in_file",
}
DEGIBBS_TO_SEP = {
    "source": DEGIBBS_NODE,
    "source_port": "out_file",
    "destination": MRCONVERT_SEPERATE_2_NODE,
    "destination_port": "in_file",
}
FMAP_TO_DWIFSLPREPROC = {
    "source": MRCONVERT_SEPERATE_1_NODE,
    "source_port": "out_file",
    "destination": DWIFSLPREPROC_NODE,
    "destination_port": "se_epi",
}
DWI_TO_DWIFSLPREPROC = {
    "source": MRCONVERT_SEPERATE_2_NODE,
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
        MIF_DWI_TO_CAT,
        MIF_FMAP_TO_CAT,
        CAT_TO_DENOISE,
        DEGIBBS_TO_SEP,
        FMAP_TO_DWIFSLPREPROC,
        DWI_TO_DWIFSLPREPROC,
        PREPROCESSED_TO_BIAS_CORRECT,
    ],
}
