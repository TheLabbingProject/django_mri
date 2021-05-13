"""
Default messages for automated anatomical preprocessing.
"""
from django_mri.analysis.automation.utils import bcolors

#: Report the successful creation of an asynchronous execution task.
EXECUTION_STARTED = (
    bcolors.OKGREEN
    + "Successfully started {analysis_version} execution over {n_scans} scans."
    + bcolors.ENDC
)

#: Report the type of filtering applied.
FILTER_QUERYSET_START = "Filtering T1-weighted scans..."

#: Reporting starting to generate input specifications for analysis execution.
INPUT_GENERATION = (
    f"{bcolors.OKBLUE}Generating input specifications...{bcolors.ENDC}"
)

#: NIfTI conversion failure message.
NIFTI_CONVERSION_FAILURE = (
    bcolors.WARNING
    + "Failed to convert scan #{instance_id} to NIfTI."
    + bcolors.ENDC
)

#: No pending scans were detected in the database.
NONE_PENDING = f"""{bcolors.OKGREEN}Congratulations! No pending scans were detected in the database 👏🚀{bcolors.ENDC}"""

#: No pending scans were detected in the provided queryset.
NONE_PENDING_IN_QUERYSET = """\033[96mAll {n_scans} provided scans have been processed already 🤷\033[0m"""

#: No T1-weighted in the database.
NO_T1_WEIGHTED = (
    bcolors.WARNING
    + "No T1-weighted scans could be detected in the database!"
    + bcolors.ENDC
)

#: Report pending scans.
PENDING_FOUND = "\033[94m{n_pending} of {n_total} scans are pending {analysis_version} execution ({n_existing} existing found).\033[0m"

#: Report number of preprocessing failures encountered.
PREPROCESSING_FAILURE_REPORT = (
    bcolors.WARNING
    + "{n_invalid} of {n_total} scans failed to be preprocessed."
    + bcolors.ENDC
)

# flake8: noqa: E501
