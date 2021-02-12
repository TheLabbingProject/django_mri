"""
WIP: utility function to load HCP archive to the database.
"""

import re
from io import StringIO
from pathlib import Path
from typing import Union
from zipfile import ZipFile

import pandas as pd

SUBJECT_FILE_REGEX = "^[0-9]{6}_3T_Structural_unproc.zip"
SUBJECT_FILE_PATTERN = re.compile(SUBJECT_FILE_REGEX)
SESSION_INFO_CSV = "{subject_id}/unprocessed/3T/{subject_id}_3T.csv"


def extract_session_info(zip_file: ZipFile, subject_id: str) -> pd.DataFrame:
    csv_path = SESSION_INFO_CSV.format(subject_id=subject_id)
    csv = StringIO(str(zip_file.read(csv_path), "utf-8"))
    return pd.read_csv(csv)


def import_hcp_subject(path: Union[Path, str]) -> pd.DataFrame:
    path = Path(path)
    valid_path = SUBJECT_FILE_PATTERN.match(str(path.name))
    if not valid_path:
        raise ValueError(f"Path does not match HCP subject data: {path}")
    subject_id = path.name.split("_")[0]
    zip_file = ZipFile(path)
    session_info = extract_session_info(zip_file, subject_id)
    for relative_path in zip_file.namelist():
        if relative_path.endswith(".nii.gz"):
            scan_path = Path(relative_path)
            scan_description = scan_path.name[10:-7]
            scan_info = session_info[
                session_info["Scan Description"] == scan_description
            ].squeeze()
            print(scan_info)

