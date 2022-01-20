"""
WIP: utility function to load HCP archive to the database.
"""
import re
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Tuple
from zipfile import ZipFile

import pandas as pd
import pytz
from django_mri.models import NIfTI, Scan, Session
from django_mri.utils import get_bids_dir, get_subject_model

SUBJECT_FILE_REGEX = "^[0-9]{6}_3T_Structural_unproc.zip"
SUBJECT_FILE_PATTERN = re.compile(SUBJECT_FILE_REGEX)
SESSION_INFO_CSV = "{subject_id}/unprocessed/3T/{subject_id}_3T.csv"
NIFTI_SUFFIX: str = ".nii.gz"
SUFFIX_LEN: int = len(NIFTI_SUFFIX)
SCAN_PREFIX_LEN: int = 10
INCLUDED_SCANS: Tuple[str] = ("T1w_MPR1", "T2w_SPC1")
MODALITY: Dict[str, str] = {"T1w_MPR1": "T1w", "T2w_SPC1": "T2w"}
SUBJECTS_CSV_NAME: str = "Subjects.csv"
TIMEZONE_ID: str = "US/Pacific"
TIMEZONE = pytz.timezone(TIMEZONE_ID)

# Session parameters
SESSION_DATES: Dict[int, datetime] = {
    1: datetime(2012, 1, 1).date(),
    2: datetime(2013, 1, 1).date(),
    3: datetime(2014, 1, 1).date(),
    4: datetime(2015, 1, 1).date(),
}

# Scan parameters
INSTITUTION_NAME: str = "HCP3T"
SCAN_PARAMETERS: Dict[str, Any] = {
    "institution_name": INSTITUTION_NAME,
}
MPRAGE_INVERSION_TIME: float = 1000.0
MPRAGE_ECHO_TIME: float = 2.14
MPRAGE_REPETITION_TIME: float = 2400.0
MPRAGE_SPATIAL_RESOLUTION: List[float] = [0.69999998807907] * 3
T2_ECHO_TIME: float = 565.0
T2_REPETITION_TIME: float = 3200.0
T2_SPATIAL_RESOLUTION: List[float] = [0.69999998807907] * 3
MODALITY_PARAMETERS: Dict[str, Dict[str, Any]] = {
    "T1w_MPR1": {
        "inversion_time": MPRAGE_INVERSION_TIME,
        "echo_time": MPRAGE_ECHO_TIME,
        "repetition_time": MPRAGE_REPETITION_TIME,
        "spatial_resolution": MPRAGE_SPATIAL_RESOLUTION,
    },
    "T2w_SPC1": {
        "echo_time": T2_ECHO_TIME,
        "repetition_time": T2_REPETITION_TIME,
        "spatial_resolution": T2_SPATIAL_RESOLUTION,
    },
}
NIFTI_TEMPLATE = (
    "sub-{pk}/ses-{session}/anat/sub-{pk}_ses-{session}_{modality}.nii.gz"
)
TIME_FORMAT: str = "%H:%M:%S"

Subject = get_subject_model()
BIDS_DIR = get_bids_dir()
PARTICIPANTS_FILE_NAME: str = "participants.tsv"
PARTICIPANTS_FILE_PATH: Path = BIDS_DIR / PARTICIPANTS_FILE_NAME


def update_participants(participant_id: str, sex: str):
    participants_df = pd.read_csv(PARTICIPANTS_FILE_PATH, sep="\t")
    existing = participants_df[
        participants_df["participant_id"] == participant_id
    ]
    if not existing.empty:
        return
    subject_dict = {"participant_id": participant_id, "sex": sex}
    participants_df = participants_df.append(
        pd.DataFrame(subject_dict, index=[0]), ignore_index=True
    )
    participants_df.to_csv(PARTICIPANTS_FILE_PATH, sep="\t", index=False)


def extract_session_info(zip_file: ZipFile, subject_id: str) -> pd.DataFrame:
    csv_path = SESSION_INFO_CSV.format(subject_id=subject_id)
    csv = StringIO(str(zip_file.read(csv_path), "utf-8"))
    return pd.read_csv(csv)


def read_subjects_info(hcp_base: Path) -> pd.DataFrame:
    return pd.read_csv(hcp_base / SUBJECTS_CSV_NAME, index_col=0)


def import_hcp_subject(
    path: Path, subjects_info: pd.DataFrame = None
) -> pd.DataFrame:
    path = Path(path)
    subject_id = int(path.name.split("_")[0])
    subjects_info = (
        subjects_info
        if subjects_info is not None
        else read_subjects_info(path.parent)
    )
    subject_info = subjects_info.loc[subject_id].squeeze()
    if isinstance(subject_info, pd.DataFrame):
        raise ValueError(f"Ambiguous subject information:\n{subject_info}")
    sex = subject_info["Gender"]
    id_number = f"HCP{subject_id}"
    subject, _ = Subject.objects.get_or_create(id_number=id_number, sex=sex)
    zip_file = ZipFile(path)
    session_info = extract_session_info(zip_file, subject_id)
    for relative_path in zip_file.namelist():
        is_nifti = relative_path.endswith(NIFTI_SUFFIX)
        if is_nifti:
            scan_path = Path(relative_path)
            scan_description = scan_path.name[SCAN_PREFIX_LEN:-SUFFIX_LEN]
            if scan_description not in INCLUDED_SCANS:
                continue
            scan_info = session_info[
                session_info["Scan Description"] == scan_description
            ].squeeze()
            scan_number = int(scan_info["Scan Number"])
            session_number = int(scan_info["Session"])
            session_time = datetime.strptime(
                session_info.loc[
                    session_info["Session"] == session_number,
                    "Acquisition Time",
                ].min(),
                TIME_FORMAT,
            ).time()
            session_date = SESSION_DATES.get(
                session_number, datetime(2015, 1, 1).date()
            )
            session_datetime = datetime.combine(
                session_date, session_time, tzinfo=TIMEZONE
            )
            session, _ = Session.objects.get_or_create(
                subject=subject, time=session_datetime
            )
            scan_time = datetime.strptime(
                scan_info["Acquisition Time"], TIME_FORMAT
            ).time()
            scan_time = datetime.combine(
                session.time.date(), scan_time, tzinfo=TIMEZONE,
            )
            modality = MODALITY[scan_description]
            destination = BIDS_DIR / NIFTI_TEMPLATE.format(
                pk=subject.id, session=session_number, modality=modality
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            with open(destination, "wb") as destination_file:
                destination_file.write(zip_file.read(relative_path))
            update_participants(f"sub-{subject.id}", sex)
            nifti, _ = NIfTI.objects.get_or_create(
                path=destination, is_raw=True
            )
            modality_parameters = MODALITY_PARAMETERS.get(scan_description, {})
            Scan.objects.get_or_create(
                session=session,
                number=scan_number,
                description=scan_description,
                time=scan_time,
                _nifti=nifti,
                **SCAN_PARAMETERS,
                **modality_parameters,
            )


def import_hcp(path: Path):
    subjects_info = read_subjects_info(path)
    for zip_path in path.rglob("*_3T_Structural_unproc.zip"):
        import_hcp_subject(zip_path, subjects_info)
