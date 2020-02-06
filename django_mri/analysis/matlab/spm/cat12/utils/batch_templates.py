from pathlib import Path

CAT12_MODULE_PATH = Path(__file__).parent.parent

CAT12_SEGMENTATION_TEMPLATE = CAT12_MODULE_PATH / "segmentation" / "batch_template.m"

CAT12_TEMPLATES = {"CAT12 Segmentation": CAT12_SEGMENTATION_TEMPLATE}

