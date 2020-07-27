"""
Definition of the
:data:`~django_mri.analysis.interfaces.matlab.spm.cat12.utils.batch_templates.CAT12_TEMPLATES`
constant, used to locate batch template file paths by interface key.
"""

from pathlib import Path

CAT12_MODULE_PATH = Path(__file__).parent.parent

CAT12_SEGMENTATION_TEMPLATE = (
    CAT12_MODULE_PATH / "segmentation" / "batch_template.m"
)

#: Batch template file path by interface (string) key.
CAT12_TEMPLATES = {"CAT12 Segmentation": CAT12_SEGMENTATION_TEMPLATE}
