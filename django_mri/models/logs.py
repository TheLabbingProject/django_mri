"""
Log message string templates for the :mod:`~django_mri.models` module.
"""
SESSION_BIDS_DELETE_START: str = "Starting BIDS directory deletion for session #{pk}"
SESSION_BIDS_DELETE_EMPTY: str = "No existing BIDS directory for session #{pk} found at {path}."
SESSION_BIDS_DELETE_END: str = "Session #{pk} BIDS directory successfully removed from {path}."
SESSION_BIDS_DELETE_FAILURE: str = "Failed to delete session #{pk}'s BIDS directory from {path} with the following exception:\n{exception}"
SESSION_NIFTI_CONVERSION_START: str = "Starting NIfTI conversion for session {pk}..."
SESSION_NIFTI_CONVERSION_END: str = "Successfully converted session {pk}'s data to NIfTI."
SESSION_NIFTI_CONVERSION_FAILURE: str = "Failed to convert session #{pk}'s data to NIfTI with the following exception:\n{exception}"
# flake8: noqa: E501
