"""
Definition of the :class:`~django_mri.analysis.interfaces.dcm2niix.Dcm2niix`
class.
"""

import re
import subprocess
import warnings

from django_mri.analysis.interfaces import messages
from pathlib import Path


#: Project's base directory.
BASE_DIR = Path(__file__).absolute().parent.parent.parent

# *dcm2niix* executable path.
DCM2NIIX = BASE_DIR / "utils" / "dcm2niix"


class Dcm2niix:
    """
    An interface for dcm2niix_.

    See Also
    --------
    * `dcm2niix user manual`_

    .. _dcm2niix:
       https://github.com/rordenlab/dcm2niix
    .. _dcm2niix user manual:
       https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage
    """

    #: Arguemnts dictionary. Keys are the interface's verbose names and values
    #: are the actual CLI's arguments.
    FLAGS = {"compressed": "-z", "BIDS": "-b", "name": "-f", "directory": "-o"}

    #: Convert boolean configurations to "y" or "n".
    BOOLEAN = {True: "y", False: "n"}

    def __init__(self, path: Path = DCM2NIIX):
        self.path = path

    def generate_command(
        self,
        path: Path,
        destination: Path,
        compressed: bool = True,
        generate_json: bool = True,
    ) -> list:
        """
        Generate the command to execute to run *dcm2niix*.

        Parameters
        ----------
        path : Path
            Input path
        destination : Path
            Output file destination
        compressed : bool, optional
            Whether to compress the file or not, by default True
        generate_json : bool, optional
            Whether to generate a JSON or not, by default True

        Returns
        -------
        list
            Command to run, split at spaces
        """

        return [
            str(self.path),
            self.FLAGS["compressed"],
            self.BOOLEAN[compressed],
            self.FLAGS["BIDS"],
            self.BOOLEAN[generate_json],
            self.FLAGS["directory"],
            str(destination.parent),
            self.FLAGS["name"],
            str(destination.name),
            str(path),
        ]

    def convert(
        self,
        path: Path,
        destination: Path,
        compressed: bool = True,
        generate_json: bool = True,
    ) -> Path:
        """
        Coverts the series in the provided *path* from DICOM to NIfTI.

        Parameters
        ----------
        path : Path
            Input DICOM directory
        destination : Path
            Output destination directory
        compressed : bool, optional
            Whether to create compressed (*.nii.gz*) files or not, by default
            True
        generate_json : bool, optional
            Whether to generate a "BIDS sidecar" JSON file with supplementary
            information, by default True

        Returns
        -------
        Path
            Output file path

        Raises
        ------
        RuntimeError
            *dcm2niix* run failure
        NotImplementedError
            *dcm2niix* executable could not be found
        """
        command = self.generate_command(
            path,
            destination,
            compressed=compressed,
            generate_json=generate_json,
        )
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            returned_path = self.extract_output_path(str(stdout), compressed)
            expected_path = destination.with_suffix(".nii.gz")
            if returned_path != expected_path:
                message = messages.DCM2NIIX_PATH_MISMATCH.format(
                    returned_path=returned_path, expected_path=expected_path,
                )
                warnings.warn(message)
            if Path(str(returned_path)).is_file():
                return returned_path
            else:
                raise RuntimeError(messages.DCM2NIIX_FAILURE)
        except FileNotFoundError:
            raise NotImplementedError(messages.NO_DCM2NIIX)

    def extract_output_path(self, stdout: str, compressed: bool) -> Path:
        """
        Returns the path of the output file.

        Parameters
        ----------
        stdout : str
            *dcm2niix* run output
        compressed : bool
            Whether the file is compressed (*.nii.gz*) or not, by default True

        Returns
        -------
        Path
            Output file path
        """

        try:
            path = re.findall(r"as (\/.*?\.[\w]+)", stdout)[0].split(" (")[0]
        except IndexError:
            return None
        ext = ".nii.gz" if compressed else ".nii"
        return Path(path).with_suffix(ext)
