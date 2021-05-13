"""
A module storing strings used to display messages.
"""

DICOM_TO_NIFTI_NO_DICOM = "Failed to convert scan #{scan_id} from DICOM to NIfTI! No DICOM series is related to this scan."
NIFTI_CONVERSION_FAILURE_HTML = "Failed to convert scan #{scan_id} to NIfTI with the following exception:<br>{exception}"
NIFTI_FILE_MISSING = "NIfTI instance #{pk} could not be located at {path}"
NO_LOCALIZER_NIFTI = "Localizer scans may not converted to NIfTI."
SUBJECT_MISMATCH = "Scan #{scan_id} already exists in the database and belongs to a different subject!\nExisting:\tSubject #{existing_subject_id}\nAssigned:\tSubject #{assigned_subject_id})"

# flake8: noqa: E501
