"""
A module storing strings used to display messages.
"""

SUBJECT_MISMATCH = "Scan #{scan_id} already exists in the database and belongs to a different subject!\nExisting:\tSubject #{existing_subject_id}\nAssigned:\tSubject #{assigned_subject_id})"
DICOM_TO_NIFTI_NO_DICOM = "Failed to convert scan #{scan_id} from DICOM to NIfTI! No DICOM series is related to this scan."
