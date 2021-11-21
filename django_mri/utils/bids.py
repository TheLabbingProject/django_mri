"""
Definition of the :class:`Bids` class.
"""
import json
import logging
import os
import re
import shutil
import warnings
from datetime import date
from pathlib import Path

import pandas as pd
from django.apps import apps
from django.db.models import Q
from django_mri.utils import logs
from django_mri.utils.messages import BIDS_NO_ACQ_LABEL
from django_mri.utils.utils import get_bids_dir

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "bids_templates"
NIfTI = apps.get_model("django_mri", "NIfTI", require_ready=False)


class BidsManager:
    """
    A class to compose BIDS-appropriate paths for usage by dcm2niix
    In short, standard template for BIDS-appropriate path is:
    *sub-<label>/<data_type>/sub-<label>_<modality_label>*

    References
    ----------
    * `The BIDS Specification`_.

    .. _The BIDS Specification:
       https://bids-specification.readthedocs.io/en/stable/
    """

    DATASET_DESCRIPTION_FILE_NAME: str = "dataset_description.json"
    PARTICIPANTS_FILE_NAME: str = "participants.tsv"
    ACQUISITION_PATTERN: str = "acq-([a-zA-Z0-9]*)"
    RUN_LABEL_PATTERN: str = "run-[0-9]*"
    RUN_LABEL_TEMPLATE: str = "run-{index}"
    NA_LABEL: str = "n/a"

    _logger = logging.getLogger("data.mri.bids")

    def calculate_age(self, born: date) -> float:
        """
        Returns age by date of birth.

        Parameters
        ----------
        born : datetime.date
            Subject's birth date

        Returns
        -------
        float
            Subject's age
        """
        today = date.today()
        try:
            return (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )
        except AttributeError:
            return self.NA_LABEL

    def get_subject_data(self, scan):
        """
        Extract related subject parameters, as included in the BIDS naming
        scheme.

        Returns
        -------
        subject_dict[dict]
            subject's relevant parameters, sorted by "participant_id",
            "handedness","age" and "sex" fields
        """
        subject = scan.session.subject
        age = self.calculate_age(subject.date_of_birth)
        subject_dict = {
            "participant_id": subject.id if subject.id else self.NA_LABEL,
            "handedness": subject.dominant_hand
            if subject.dominant_hand
            else self.NA_LABEL,
            "age": age,
            "sex": subject.sex if subject.sex else self.NA_LABEL,
        }
        return subject_dict

    def build_bids_path(self, scan):
        """
        Uses parameters extracted by :func:`get_subject_data` to update BIDS-
        compatible file path derived from *dicom_parser*

        Returns
        -------
        pathlib.Path
            Full path to an updated BIDS-compatible file, according to scan's
            parameters.
        """
        # Log start.
        start_log = logs.BUILD_BIDS_PATH_START.format(scan_id=scan.id)
        self._logger.debug(start_log)

        # Query naive relative BIDS path, as returned by dicom_parser.
        sample_header = scan.dicom.get_sample_header()
        default_bids_path = sample_header.build_bids_path()
        # If no naive BIDS path could be generated, show warning.
        if default_bids_path is None:
            no_bids_log = logs.NO_BIDS_PATH.format(
                scan_id=scan.id, description=scan.description
            )
            warnings.warn(no_bids_log)
            return
        # Log the returned naive BIDS path.
        naive_bids_log = logs.NAIVE_BIDS.format(
            relative_path=default_bids_path
        )
        self._logger.debug(naive_bids_log)

        # Replace patient ID with subject primary key.
        subject_id = scan.session.subject.id
        patient_id = sample_header.get("PatientID")
        subject_fix_log = logs.SUBJECT_FIX.format(
            patient_id=patient_id, subject_id=subject_id
        )
        self._logger.debug(subject_fix_log)
        fixed_relative_path = default_bids_path.replace(
            f"sub-{patient_id}", f"sub-{subject_id}"
        )
        bids_path = get_bids_dir() / fixed_relative_path
        single_run_destination_log = logs.SINGLE_RUN_DESTINATION.format(
            scan_id=scan.id, destination=bids_path
        )
        self._logger.debug(single_run_destination_log)

        # Check for existing runs with the same acquisition parameters.
        parts = str(bids_path).split("_")
        acquisition_labels = "_".join(parts[:-1])
        datatype = parts[-1]
        existing_query = Q(path__contains=acquisition_labels) & Q(
            path__contains=datatype
        )
        self._logger.debug(
            f"Checking for an existing NIfTI files with identical labels ({acquisition_labels})"  # noqa: E501
        )
        existing = NIfTI.objects.filter(existing_query)
        if not existing.exists():
            self._logger.debug("No existing NIfTI file found! All done.")
            return bids_path
        else:
            if existing.count() == 1:
                existing = existing.first()
                bids_path = Path(existing.path.split(".")[0])
                self._logger.debug(
                    f"Existing NIfTI (#{existing.id}) found at {existing.path}!"  # noqa: E501
                )
                if scan._nifti == existing:
                    self._logger.debug(
                        "Existing NIfTI instance belongs to queried scan!"
                    )
                    return bids_path
                self._logger.debug(
                    f"Checking for an existing run label in scan #{scan.id}."
                )
                try:
                    existing_run_label = re.findall(
                        self.RUN_LABEL_PATTERN, str(bids_path)
                    )[0]
                except IndexError:
                    self._logger.debug("No existing run label found.")
                    self._logger.debug(
                        f"Renaming existing NIfTI (#{existing.id}) to include run label."  # noqa: E501
                    )
                    existing_run_label = self.RUN_LABEL_TEMPLATE.format(
                        index=1
                    )
                    name_parts = Path(existing.path).name.split("_")
                    name_parts.insert(-1, existing_run_label)
                    name_with_run = "_".join(name_parts)
                    updated_path = bids_path.parent / name_with_run
                    existing.rename(updated_path)
                    self._logger.debug(
                        f"Scan #{scan.id} successfully moved to {bids_path}"
                    )
                    new_run_label = self.RUN_LABEL_TEMPLATE.format(index=2)
                    bids_path = (
                        updated_path.parent / updated_path.name.split(".")[0]
                    )
                else:
                    self._logger.debug(
                        f"Existing run label found: {existing_run_label}"
                    )
                    existing_run_index = int(existing_run_label.split("-"))
                    index = existing_run_index + 1
                    new_run_label = self.RUN_LABEL_TEMPLATE.format(index=index)
                    self._logger.debug(f"New run label: {new_run_label}")
            else:
                self._logger.debug(
                    "Multiple existing NIfTI files found with the queried parameters."  # noqa: E501
                )
                run_labels = (
                    re.findall(self.RUN_LABEL_PATTERN, str(nii.path))
                    for nii in existing
                )
                run_indices = [
                    int(label[0].split("-")[-1])
                    for label in run_labels
                    if label != []
                ]
                self._logger.debug(
                    f"Found existing run indices: {run_indices}"
                )
                index = max(run_indices) + 1
                new_run_label = self.RUN_LABEL_TEMPLATE.format(index=index)
                name_parts = Path(bids_path).name.split("_")
                name_parts.insert(-1, new_run_label)
                name_with_run = "_".join(name_parts)
                self._logger.debug(
                    f"Updated current file name to: {name_with_run}"
                )
                return bids_path.parent / name_with_run
            return Path(
                str(bids_path).replace(existing_run_label, new_run_label)
            )

    def fix_functional_json(self, bids_path: Path):
        """
        Add required "TaskName" field to functional scan, as stated in BIDS
        stucture.

        Parameters
        ----------
        bids_path : Path
            Path to the BIDS-compatible directory

        References
        ----------
        * `BIDS MRI specification`_

        .. _BIDS MRI specification:
            https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html
        """
        bids_path = Path(bids_path)
        task = str(bids_path).split("task-")[-1].split("_")[0]
        json_file = bids_path.parent / f"{bids_path.name.split('.')[0]}.json"
        with open(json_file, "r+") as f:
            data = json.load(f)
            data["TaskName"] = task
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def modify_fieldmaps(self, bids_path):
        """
        Add required "IntendedFor" field to fieldmaps, as stated in BIDS
        stucture.

        Parameters
        ----------
        bids_path : Path
            Path to the BIDS-compatible directory

        References
        ----------
        * `BIDS MRI specification`_

        .. _BIDS MRI specification:
            https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html
        """
        base_name = bids_path.name.split(".")[0]
        json_path = bids_path.parent / f"{base_name}.json"
        data_type_target = re.findall(self.ACQUISITION_PATTERN, base_name)
        if data_type_target == []:
            message = BIDS_NO_ACQ_LABEL.format(base_name=base_name)
            print(message)
        else:
            data_type_target = data_type_target[0]
        session_dir = json_path.parent.parent
        target_pattern = f"{data_type_target}/*.nii*"
        targets = [p for p in session_dir.glob(target_pattern)]

        if targets:
            fin = open(json_path, "r")
            data = json.load(fin)
            fin.close()
            data["IntendedFor"] = [
                os.sep.join(target.parts[-3:]) for target in targets
            ]
            fout = open(json_path, "w")
            json.dump(data, fout, indent=4)
            fout.close()
        else:
            warnings.warn(f"No target file for {bids_path} could be found!")

    def set_participant_tsv_and_json(self, scan):
        """
        Generates recommended "participants.tsv" by either copying the
        template from TEMPLATES_DiR or editing an existing one under {parent}
        directory.

        Parameters
        ----------
        parent : Path
            BIDS-compatible directory, underwhich there are "sub-x" directories
        subject_dict : dict
            Subject's parameters dictionary, containing "participant_id",
            "handedness","age","sex" fields

        References
        ----------
        * `BIDS complementary files`_

        .. _BIDS complementary files:
            https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html
        """
        bids_dir = get_bids_dir()
        bids_dir.mkdir(exist_ok=True, parents=True)

        subject_dict = self.get_subject_data(scan)

        participants_tsv = bids_dir / self.PARTICIPANTS_FILE_NAME
        participants_json = participants_tsv.with_suffix(".json")
        for participants_file in [participants_tsv, participants_json]:
            if not participants_file.is_file():
                participants_template = TEMPLATES_DIR / participants_file.name
                shutil.copy(str(participants_template), str(participants_file))
        participants_df = pd.read_csv(participants_tsv, sep="\t")
        subject_dict[
            "participant_id"
        ] = f"sub-{subject_dict['participant_id']}"
        if (
            not subject_dict["participant_id"]
            in participants_df["participant_id"].values
        ):
            participants_df = participants_df.append(
                pd.DataFrame(subject_dict, index=[0]), ignore_index=True
            )
            participants_df.to_csv(participants_tsv, sep="\t", index=False)
        else:
            pass

    def set_description_json(self):
        """
        Generates required "dataset_description.json" file, as stated by BIDS
        structure.

        References
        ----------
        * `BIDS complementary files`_

        .. _BIDS complementary files:
            https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html
        """
        bids_dir = get_bids_dir()
        bids_dir.mkdir(exist_ok=True, parents=True)
        description_file = bids_dir / self.DATASET_DESCRIPTION_FILE_NAME
        if not description_file.is_file():
            description_template = TEMPLATES_DIR / description_file.name
            description_file.parent.mkdir(exist_ok=True)
            shutil.copy(str(description_template), str(description_file))

    def generate_bidsignore(self):
        """
        Some acquisitions do not conform to BIDS specification (mainly
        localizers), so we generate a .bidsignore file, pointing to them.

        References
        ----------
        * `BIDS validator specifications`_

        .. _BIDS validator specifications:
            https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/bids-validator.html
        """
        bids_dir = get_bids_dir()
        bids_dir.mkdir(exist_ok=True, parents=True)
        bidsignore = bids_dir / ".bidsignore"
        with open(bidsignore, "w+") as in_file:
            in_file.write("**/*ignore-bids*\n")

    def generate_readme(self):
        """
        It is recommended by BIDS specifications to have a README file at the
        base of our project, so we create a blank one for further usage.
        """
        bids_dir = get_bids_dir()
        bids_dir.mkdir(exist_ok=True, parents=True)
        readme = bids_dir / "README"
        if not readme.is_file():
            readme_template = TEMPLATES_DIR / "README"
            shutil.copy(str(readme_template), str(readme))

    def scaffold_bids_directory(self):
        """
        Initiate necessery BIDS directory files
        """
        self.set_description_json()
        self.generate_bidsignore()
        self.generate_readme()
