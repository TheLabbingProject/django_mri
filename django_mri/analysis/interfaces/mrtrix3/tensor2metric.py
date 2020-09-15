"""
Definition of the
:class:`~django_mri.analysis.interfaces.mrtrix3.tensor2metric` interface.
"""

import os
from pathlib import Path


class Tensor2metric:
    """
    An interface for the MRtrix3 *tensor2metric* script.

    References
    ----------
    * tensor2metric_

    .. _tensor2metric:
       https://mrtrix.readthedocs.io/en/latest/reference/commands/tensor2metric.html
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
    DEFAULT_OUTPUTS = {
        "adc": "MD.nii.gz",
        "fa": "FA.nii.gz",
        "ad": "AD.nii.gz",
        "rd": "RD.nii.gz",
        "cl": "CL.nii.gz",
        "cp": "CP.nii.gz",
        "cs": "CS.nii.gz",
    }

    __version__ = "BETA"

    def __init__(self, **kwargs):
        self.configuration = kwargs

    def add_outputs(self, destination: Path) -> dict:
        """
        Adds the *metrics* output files to the interface's configuration before
        generating the command to run.

        References
        ----------
        * metrics_

        .. _metrics:
            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3163395/

        Parameters
        ----------
        destination : Path
            Output directory

        Returns
        -------
        dict
            Updated configuration dictionary
        """

        config = self.configuration.copy()
        for key in self.DEFAULT_OUTPUTS:
            if key not in config.keys():
                config[key] = destination / config[key]
        return config

    def set_configuration_by_keys(self, config: dict):
        key_command = ""
        for key, value in config.items():
            key_addition = f" -{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self, destination: Path, config: dict) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Parameters
        ----------
        destination : Path
            Output files destination direcotry
        config : dict
            Configuration arguments for the command

        Returns
        -------
        str
            Complete execution command
        """

        # output_path = destination / self.DEFAULT_OUTPUT_NAME
        in_file = config.pop("in_file")
        command = f"tensor2metric {in_file}"
        return command + self.set_configuration_by_keys(config)


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
        for key, val in self.DEFAULT_OUTPUTS:
            output_dict[key] = destination / val
        return output_dict

    def run(self, destination: Path = None) -> dict:
        """
        Runs *dwifslpreproc* with the provided *scan* as input.
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
        in_file = self.configuration.pop("in_file")
        destination = (
            Path(destination) if destination else Path(in_file).parent
        )
        config = self.add_outputs(destination)
        command = self.generate_command(destination, config)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run tensor2metric!\nExecuted command: {command}"
            )
        return self.generate_output_dict(destination)
