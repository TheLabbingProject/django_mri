"""
Definition of the :class:`Bids` class.
"""

import glob
import json
import os
import shutil
from datetime import date
from enum import Enum
from pathlib import Path

import pandas as pd
from django_mri.utils import messages, the_base, get_bids_dir

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "bids_templates"


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

    DATASET_DESCRIPTION_FILE_NAME = "dataset_description.json"
    PARTICIPANTS_FILE_NAME = "participants.tsv"

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
            age = (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )
        except AttributeError:
            age = "n/a"
        return age

    def get_subject_data(self, scan):
        """
        Extract relevant Scan-related subject's parameters, as stated by BIDS
        structure.

        Returns
        -------
        subject_dict[dict]
            subject's relevant parameters, sorted by "participant_id",
            "handedness","age" and "sex" fields
        """

        subject = scan.session.subject
        age = self.calculate_age(subject.date_of_birth)
        subject_dict = {
            "participant_id": subject.id if subject.id else "n/a",
            "handedness": subject.dominant_hand
            if subject.dominant_hand
            else "n/a",
            "age": age,
            "sex": subject.sex if subject.sex else "n/a",
        }
        return subject_dict

    def build_bids_path(self, scan):
        """
        Uses parameters extracted by {self.get_subject_data} to update BIDS-
        compatible file path derived from *dicom_parser*

        Returns
        -------
        pathlib.Path
            Full path to an updated BIDS-compatible file, according to scan's
            parameters.
        """

        subject_id = scan.session.subject.id
        sample_image = scan.series.image_set.first()
        sample_header = sample_image.header.instance
        default_bids_path = sample_header.bids_path
        default_subject_id = sample_header.get("PatientID")
        return default_bids_path.replace(
            f"sub-{default_subject_id}", f"sub-{subject_id}"
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
        json_file = bids_path.parent / f"{bids_path.name.split('.')}.json"
        with open(json_file, "r+") as f:
            data = json.load(f)
            data["TaskName"] = task
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def modify_fieldmaps(self, scan):
        """
        Add required "IntendedFor" field to fieldmaps, as stated in BIDS
        stucture.

        Parameters
        ----------
        scan : Scan object
            *django_mri*`s Scan object

        References
        ----------
        * `BIDS MRI specification`_

        .. _BIDS MRI specification:
            https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html
        """

        bids_path = Path(scan.get_bids_destination())
        bids_path = bids_path.parent / f"{bids_path.name.split('.')[0]}.json"
        parts = bids_path.name.split("_")
        data_type_target = [
            part.split("-")[-1] for part in parts if "acq-" in part
        ]
        targets = [
            p
            for p in bids_path.parents[1].glob(f"{data_type_target[0]}/*.nii*")
        ]

        fin = open(bids_path, "r")
        data = json.load(fin)
        fin.close()
        data["IntendedFor"] = [
            os.sep.join(target.parts[-3:]) for target in targets
        ]
        fout = open(bids_path, "w")
        json.dump(data, fout, indent=4)
        fout.close()

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
        participants_df = pd.read_csv(participants_tsv, "\t")
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
            in_file.write("**/*ignore-bids*")
            in_file.write("**/*IREPI*")

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

    def initiate_bids_directory(self):
        """
        Initiate necessery BIDS directory files
        """
        self.bids_manager.set_description_json()
        self.bids_manager.generate_bidsignore()
        self.bids_manager.generate_readme()
