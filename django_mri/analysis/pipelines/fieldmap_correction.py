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
BET_CONFIGURATION = {}

FSLROI_NODE = {
    "analysis_version": "fslroi",
    "configuraion": FSLROI_CONFIGURATION,
}
MERGE_NODE = {
    "analysis_version": "merger",
    "configuration": MERGE_CONFIGURATION,
}
TOPUP_NODE = {"analysis_version": "topup", "coniguration": TOPUP_CONFIGURATION}
BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}

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

