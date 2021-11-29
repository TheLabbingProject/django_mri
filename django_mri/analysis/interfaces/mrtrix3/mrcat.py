"""
Definition of the
:class:`~django_mri.analysis.interfaces.mrtrix3.mrcat` interface.
"""

import os
from pathlib import Path


class MRCat:
    """
    An interface for the MRtrix3 *dwi2tensor* script.

    References
    ----------
    * mrcat_

    .. mrcat:
       https://mrtrix.readthedocs.io/en/latest/reference/commands/mrcat.html
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.
    FLAGS = (
        "force",
        "quiet",
        "info",
        "nocleanup",
    )
    #: Default name for primary output files.
    DEFAULT_OUTPUTS = {"out_file": "concatenated.mif"}

    __version__ = "BETA"

    def __init__(self, **kwargs):
        self.configuration = kwargs

    def set_configuration_by_keys(self, config: dict):
        key_command = ""
        for key, value in config.items():
            key_addition = f" -{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            elif key in self.FLAGS and value:
                pass
            elif key in self.FLAGS:
                key_addition = ""
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self, config: dict) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Parameters
        ----------
        destination : Path
            Output files destination directory
        config : dict
            Configuration arguments for the command

        Returns
        -------
        str
            Complete execution command
        """
        # output_path = destination / self.DEFAULT_OUTPUT_NAME
        in_files = config.pop("in_files")
        out_file = config.pop("out_file")
        command = f"mrcat" + self.set_configuration_by_keys(config)
        for f in in_files:
            command += f" {f}"
        command += f" {out_file}"
        return command

    def generate_output_dict(self, destination: Path) -> dict:
        """
        Generates a dictionary of the expected output file paths by key.

        Parameters
        ----------
        destination : Path
            Output files destination directory

        Returns
        -------
        dict
            Output files by key
        """

        output_dict = {}
        for key, val in self.DEFAULT_OUTPUTS.items():
            output_dict[key] = destination / val
        return output_dict

    def run(self) -> dict:
        """
        Runs *mrcat* with the provided *in_files* as input.
        If *destination* is not specified, output files will be created within
        *scan*\'s directory.

        Parameters
        ----------
        scan : ~django_mri.models.scan.Scan
            Input scan
        destination : Path, optional
            Output files destination directory, by default None

        Returns
        -------
        dict
            Output files by key

        Raises
        ------
        RuntimeError
            Run failure
        """
        destination = Path(self.configuration.get("out_file")).parent
        command = self.generate_command(self.configuration)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run mrcat!\nExecuted command: {command}"
            )
        return self.generate_output_dict(destination)
