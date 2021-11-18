"""
Definition of the :class:`Bids` class.
"""
import json
import os
import re
import shutil
import warnings
from datetime import date
from pathlib import Path

import pandas as pd
from django_mri.utils.messages import BIDS_NO_ACQ_LABEL
from django_mri.utils.utils import get_bids_dir

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

    DATASET_DESCRIPTION_FILE_NAME: str = "dataset_description.json"
    PARTICIPANTS_FILE_NAME: str = "participants.tsv"
    ACQUISITION_PATTERN: str = "acq-([a-zA-Z0-9]*)"
    NA_LABEL: str = "n/a"

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
        subject_id = scan.session.subject.id
        sample_image = scan.dicom.image_set.first()
        sample_header = sample_image.header.instance
        default_bids_path = sample_header.build_bids_path()
        default_subject_id = sample_header.get("PatientID")
        if default_bids_path is None:
            raise ValueError
        return get_bids_dir() / Path(
            default_bids_path.replace(
                f"sub-{default_subject_id}", f"sub-{subject_id}"
            )
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
        session_dir = json_path.parents[1]
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
