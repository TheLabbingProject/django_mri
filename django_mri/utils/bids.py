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
from django_mri.utils import messages, the_base

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
        data_type = bids_path.parent.name
        if data_type == "func":
            task = str(bids_path).split("task-")[-1].split("_")[0]
            json_file = bids_path.parent / Path(bids_path.stem).with_suffix(
                ".json"
            )
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
        bids_path : Path
            Path to the BIDS-compatible directory

        References
        ----------
        * `BIDS MRI specification`_

        .. _BIDS MRI specification:
            https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html
        """

        session = scan.session
        session_id = session.time.strftime("%Y%M%d%H%m")
        bids_path = Path(scan.get_bids_destination())
        parts = bids_path.name.split("_")
        data_type_target = [
            part.split("-")[-1] for part in parts if "acq-" in part
        ]
        targets = [
            p for p in bids_path.parent.glob(f"{data_type_target[0]}/*.nii*")
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

    def set_description_json(self, parent: Path):
        """
        Generates required "dataset_description.json" file, as stated by BIDS
        structure.

        Parameters
        ----------
        parent : Path
            BIDS-compatible directory, underwhich there are "sub-x"
            directories

        References
        ----------
        * `BIDS complementary files`_

        .. _BIDS complementary files:
            https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html
        """

        description_file = parent / self.DATASET_DESCRIPTION_FILE_NAME
        if not description_file.is_file():
            description_template = TEMPLATES_DIR / description_file.name
            description_file.parent.mkdir(exist_ok=True)
            shutil.copy(str(description_template), str(description_file))

    def fix_sbref(self, bids_path: Path):
        """[summary]

        Parameters
        ----------
        bids_path : Path
            [description]
        """
        modality = bids_path.name.split("_")[-1]
        if "sbref" in modality:
            target = [f for f in bids_path.parent.glob("*_bold.nii*")]
            sbrefs = [f for f in bids_path.parent.glob("*_sbref*")]
            if target:
                acq = target[0].name.split("_")[3]
                for sbref in sbrefs:
                    parts = sbref.name.split("_")
                    new_sbref = sbref.parent / "_".join(
                        parts[:3] + [acq] + parts[4:]
                    )
                    os.rename(sbref, new_sbref)
        else:
            sbref = [f for f in bids_path.parent.glob("*_sbref.json")]
            if sbref:
                self.fix_sbref(sbref[0].parent / sbref[0].stem)

    def set_participant_tsv_and_json(self, parent: Path, subject_dict: dict):
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

        participants_tsv = parent / self.PARTICIPANTS_FILE_NAME
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

    def generate_bidsignore(self, parent: Path):
        """
        Some acquisitions do not conform to BIDS specification (mainly
        localizers), so we generate a .bidsignore file, pointing to them.

        Parameters
        ----------
        parent : Path
            BIDS-compatible directory, underwhich there are "sub-x" directories

        References
        ----------
        * `BIDS validator specifications`_

        .. _BIDS validator specifications:
            https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/bids-validator.html
        """

        bidsignore = parent / ".bidsignore"
        with open(bidsignore, "w+") as in_file:
            in_file.write("**/*ignore-bids*")
            in_file.write("**/*IREPI*")

    def generate_readme(self, parent: Path):
        """
        It is recommended by BIDS specifications to have a README file at the
        base of our project, so we create a blank one for further usage.

        Parameters
        ----------
        parent : Path
            BIDS-compatible directory, underwhich there are "sub-x" directories
        """

        readme = parent / "README"
        if not readme.is_file():
            readme_template = TEMPLATES_DIR / "README"
            shutil.copy(str(readme_template), str(readme))
