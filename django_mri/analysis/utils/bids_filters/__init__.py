from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).parent
FMRIPREP_FILTERS = Path(f"{CURRENT_DIRECTORY}/fmriprep.json").absolute()
DMRIPREP_FILTERS = Path(f"{CURRENT_DIRECTORY}/dmriprep.json").absolute()
