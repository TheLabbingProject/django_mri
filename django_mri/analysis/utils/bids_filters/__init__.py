from pathlib import Path

CURRENT_DIRECTORY = Path(__file__).parent
DMRIPREP_FILTERS = Path(f"{CURRENT_DIRECTORY}/dmriprep.json").absolute()
FMRIPREP_FILTERS = Path(f"{CURRENT_DIRECTORY}/fmriprep.json").absolute()
QSIPREP_FILTERS = Path(f"{CURRENT_DIRECTORY}/qsiprep.json").absolute()
