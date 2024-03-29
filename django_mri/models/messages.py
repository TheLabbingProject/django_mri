"""
A module storing strings used to display messages.
"""
BRAIN_REGION_KEY: str = "Brain region defintion must include a title or an index."
DICOM_TO_NIFTI_NO_DICOM: str = "Failed to convert scan #{scan_id} from DICOM to NIfTI! No DICOM series is related to this scan."
SCAN_UPDATE_NO_DICOM: str = "No DICOM data associated with MRI scan {pk}!"
NIFTI_CONVERSION_FAILURE_HTML: str = "Failed to convert scan #{scan_id} to NIfTI with the following exception:<br>{exception}"
NIFTI_FILE_MISSING: str = "NIfTI instance #{pk} could not be located at {path}"
PROCESSED_SEQUENCE_TYPE: str = "Sequence type can only be infered for unprocessed NIfTI instances."
NO_LOCALIZER_NIFTI: str = "Localizer scans may not converted to NIfTI."
SUBJECT_MISMATCH: str = "Scan #{scan_id} already exists in the database and belongs to a different subject!\nExisting:\tSubject #{existing_subject_id}\nAssigned:\tSubject #{assigned_subject_id})"

# flake8: noqa: E501
