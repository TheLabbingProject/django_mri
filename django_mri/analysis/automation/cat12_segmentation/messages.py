"""
CAT12 segmentation automation module messages.
"""
from django_mri.analysis.automation.utils import bcolors

#: NIfTI conversion failure message.
CONVERSION_FAILURE = "Failed to convert scan #{scan_id} to NIfTI."

#: Report number of conversion failures encountered.
INVALID_INPUTS = (
    bcolors.WARNING
    + "{n_invalid} of {n_total} scans failed to be prepared for CAT12 segmentation."
    + bcolors.ENDC
)

#: No anatomicals in the database.
NO_T1_WEIGHTED = (
    bcolors.WARNING
    + "No anatomical scans could be detected in the database!"
    + bcolors.ENDC
)

#: No pending scans were detected in the database.
NO_PENDING_ANATOMICALS = f"""
{bcolors.OKCYAN}Congratulations! No pending anatomical scans were detected in the database 👏{bcolors.ENDC}

{bcolors.BOLD}To query existing runs:{bcolors.ENDC}
>>> from django_mri.analysis.automation.cat12_segmentation.utils import get_node
>>> cat_node = get_node()
>>> runs = cat_node.run_set.all()

{bcolors.BOLD}To query a particular run's output use the run model's get_output() method:{bcolors.ENDC}
>>> runs[0].get_output("warped_image")
'/path/to/run_dir/mri/wmscan.nii'
"""

#: No pending scans were detected in the provided queryset.
NO_PENDING_IN_QUERYSET = """
\033[96mAll {n_scans} provided scans have been processed already 👍\033[0m

\033[1mTo query results (assuming some processed `scan` instance):\033[0m
>>> from django_mri.analysis.automation.cat12_segmentation.utils import get_node
>>> cat_node = get_node()
>>> input_spec = {{'path': scan.nifti.path}}
>>> run = cat_node.get_run_by_input(input_spec).first()
>>> run.get_output("warped_image")
'/path/to/run_dir/mri/wmscan.nii'
"""

# flake8: noqa: E501
