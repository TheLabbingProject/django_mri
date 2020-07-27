"""
Definition of the :class:`~django_mri.utils.bids.Bids` class.
"""

import glob
import json
import os
import pandas as pd
import shutil

from datetime import date
from django_mri.utils import messages
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "bids_templates"


class DATA_TYPES(Enum):
    dwi = "dwi"
    AP = "dwi"
    PA = "fmap"
    mprage = "anat"
    flair = "anat"
    fmri = "func"
    ir_epi = "anat"
    ir_epi2 = "anat"
    localizer = "anat"


class MODALITY_LABELS(Enum):
    dwi = "dwi"
    AP = "dwi"
    PA = "epi"
    mprage = "T1w"
    ir_epi = "T1w"
    ir_epi2 = "T1w"
    flair = "FLAIR"
    fmri = "bold"
    localizer = "localizer"


class Bids:
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

    def __init__(self, scan):
        self.scan = scan

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

    def get_subject_data(self):
        """
        Extract relevant Scan-related subject's parameters, as stated by BIDS
        structure.

        Returns
        -------
        subject_dict[dict]
            subject's relevant parameters, sorted by "participant_id",
            "handedness","age" and "sex" fields
        """

        subject = self.scan.subject
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

    def get_data(self):
        """
        Extracts relevant parameters for BIDS-compatible naming.

        Todo
        ----
        * Update to handle several tasks.
        * Update to handle multiple sessions. - Perhaps add "session" property
            to Scan.

        Returns
        -------
        parent : Path
            Parent BIDS directory, under which there will be "sub-x"
            directories
        data_type : str
            sub-directory under "sub-x". either "anat","func","fmap" or "dwi"
        modality_label : str
            modality label as described in BIDS specifications. either "dwi",
            "epi","T1w","FLAIR","bold" or "localizer"
        task : Union[str, None]
            task name for functional scans. "rest" or None
        pe_dir : Union[str, None]
            PhaseEncodingDirection for DWI-related images or fieldmap-related
            images. Either "AP","PA" or None
        """

        sequence_type = self.scan.sequence_type
        if sequence_type is None:
            raise ValueError(messages.BIDS_NO_SEQUENCE_TYPE)
        sequence_type = str(sequence_type).lower().replace("-", "_")
        data_type = DATA_TYPES[sequence_type].value
        modality_label = MODALITY_LABELS[sequence_type].value
        dicom_image = self.scan.dicom.image_set.first()
        header = dicom_image.header.instance
        parent = self.scan.get_default_nifti_destination().parent.parent.parent
        acq = None
        task = None
        pe_dir = None
        if "dwi" in data_type:
            image_type = header["ImageType"]
            pe_dir = "AP" if "MOSAIC" in image_type else "PA"
            data_type = DATA_TYPES[pe_dir].value
            modality_label = MODALITY_LABELS[pe_dir].value
        if "anat" in data_type and "T1w" in modality_label:
            image_type = header["ImageType"]
            if sequence_type == "mprage":
                if "NORM" in image_type:
                    acq = "corrected"
                else:
                    acq = "uncorrected"
            elif "ir_epi" in sequence_type:
                ti = int(header["InversionTime"])
                acq = f"IREPI{ti}"
        if "localizer" in modality_label:
            acq = "ignore-bids"
        if "func" in data_type:
            image_type = header["ImageType"]
            task = "rest"
            if "MB" not in image_type:
                modality_label = "sbref"
        return parent, data_type, modality_label, acq, task, pe_dir

    def compose_bids_path(self):
        """
        Uses parameters extracted by {self.get_data} to compose a BIDS-
        compatible file path

        Returns
        -------
        pathlib.Path
            Full path to a BIDS-compatible file, according to scan's
            parameters.
        """

        subject_dict = self.get_subject_data()
        subject_id = subject_dict["participant_id"]
        parent, data_type, modality_label, acq, task, pe_dir = self.get_data()
        bids_path = Path(
            parent, f"sub-{subject_id}", data_type, f"sub-{subject_id}"
        )
        if acq:
            bids_path = Path(f"{bids_path}_acq-{acq}")
        if task:
            bids_path = Path(f"{bids_path}_task-{task}")
        if pe_dir:
            bids_path = Path(f"{bids_path}_dir-{pe_dir}")
        bids_path = Path(f"{bids_path}_{modality_label}")
        self.set_description_json(parent)
        self.set_participant_tsv_and_json(parent, subject_dict)
        self.generate_bidsignore(parent)
        self.generate_readme(parent)
        return bids_path

    def clean_unwanted_files(self, bids_path: Path):
        """
        Clean irrelevant .bvec and .bval files;
        Some versions of dcm2niix produce .bvec and .bval for fieldmap images
        as well as dwi images.
        Since BIDS specifications do now allow such files under "fmap"
        data-type, this method deletes them from the relevant directory.

        Parameters
        ----------
        bids_path : Path
            Path to the BIDS-compatible directory
        """

        if "fmap" in str(bids_path):
            unwanted = glob.glob(f"{str(bids_path.parent)}/*.bv*")
            for fname in unwanted:
                os.remove(fname)

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
        if "func" in str(bids_path):
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
