"""
Definition of the :class:`MRIQC` interface.
"""
import os
from pathlib import Path
from typing import Tuple

from django_mri.analysis.interfaces.mriqc.messages import RUN_FAILURE
from django_mri.analysis.interfaces.mriqc.utils import COMMAND, FLAGS
from django_mri.utils import get_singularity_root


class MRIQC:
    """
    An interface for the *mriqc* quality-control pipeline.
    """

    #: Binary configurations.
    FLAGS = FLAGS

    __version__ = None

    def __init__(self, **kwargs):
        """
        Initializes a new :class:`MRIQC` interface instance.
        """
        self.nifti_root, self.analysis_root = self.set_input_and_output_roots()
        self.destination = self.analysis_root / kwargs.pop("destination")
        self.configuration = kwargs

    def set_input_and_output_roots(self) -> Tuple[Path, Path]:
        """
        Sets the input and output directories to be mounted by singularity

        Returns
        -------
        Tuple[Path, Path]
            Paths to input and output directories, accordingly
        """
        from django_mri.utils import get_mri_root

        mri_root = get_mri_root()
        return mri_root / "rawdata", mri_root.parent / "analysis"

    def set_configuration_by_keys(self):
        """
        Builds command for fmriprep CLI (via singularity) based on user's
        specifications.

        Returns
        -------
        str
            CLI-compatible command
        """
        key_command = ""
        for key, value in self.configuration.items():
            key_addition = f" --{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            elif key in self.FLAGS and value:
                pass
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Returns
        -------
        str
            Complete execution command
        """
        analysis_level = self.configuration.pop("analysis_level")
        singularity_image_root = get_singularity_root()
        command = COMMAND.format(
            bids_parent=self.nifti_root.parent,
            destination_parent=self.destination.parent,
            bids_name=self.nifti_root.name,
            destination_name=self.destination.name,
            analysis_level=analysis_level,
            version=self.__version__,
            singularity_image_root=singularity_image_root,
        )
        return command + self.set_configuration_by_keys()

    def generate_output_dict(self) -> dict:
        """
        Generates a dictionary of the expected output file paths by key.

        Returns
        -------
        dict
            Output files by key
        """
        output_dict = {}
        output_dict["scores"] = [
            str(path) for path in self.destination.rglob("*.json")
        ]
        output_dict["reports"] = [
            str(path) for path in self.destination.glob("*.html")
        ]
        output_dict["logs"] = [
            str(path) for path in self.destination.glob("logs/*")
        ]
        return output_dict

    def run(self) -> dict:
        """
        Runs *fmriprep* with the provided *bids_dir* as input.
        If *destination* is not specified, output files will be created within
        *bids_dir*\'s parent directory.

        Returns
        -------
        dict
            Dictionary with keys and values corresponding to descriptions and
            files of *fmriprep*\'s outputs accordingly

        Raises
        ------
        RuntimeError
            In case of failed execution, raises an appropriate error
        """
        command = self.generate_command()
        raised_exception = os.system(command)
        if raised_exception:
            message = RUN_FAILURE.format(
                command=command, exception=raised_exception
            )
            raise RuntimeError(message)
        return self.generate_output_dict()


class MRIQC2100rc2(MRIQC):
    __version__ = "21.0.0rc2"


# TODO TEST singuldary
