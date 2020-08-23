"""
Definition of the
:class:`~django_mri.analysis.interfaces.fsl.generate_datain` interface.
"""

import subprocess

from pathlib import Path


class GenerateDatain:
    """
    An interface for automatically create a datain.txt file for field map correction by FSL's tools.

    References
    ----------
    * Field map correction with FSL_

    .. _Field map correction with FSL:
       https://lcni.uoregon.edu/kb-articles/kb-0003
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.

    #: Non-default output configurations.
    #: Default name for primary output file.

    __version__ = "BETA"

    def __init__(self, configuration: dict):
        self.configuration = configuration

    def add_supplementary_outputs(self, destination: Path) -> dict:
        """
        Adds the *eddy* output files to the interface's configuration before
        generating the command to run.

        References
        ----------
        * eddy_

        .. _eddy:
            https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy

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
        for key in self.SUPPLEMENTARY_OUTPUTS:
            if key not in config.keys():
                config[key] = destination
        return config

    def set_default_configurations(self, scan, configurations: dict) -> dict:
        """
        Sets default values for convenience of use.
        Parameters
        ----------
        scan : ~django_mri.models.scan.Scan
            Input scan
        configurations : dict
            Dictionary of configuration arguments for the command by keys and values

        Returns
        -------
        dict
            Default input files by key if not stated by user
        """
        for key, value in configurations.items():
            if key in self.DEFAULT_INPUTS and not value:
                if "json" in key:
                    configurations[key] = scan.nifti.json_file
                elif "grad" in key:
                    configurations[
                        key
                    ] = f"{scan.nifti.b_vector_file} {scan.nifti.b_value_file}"
        return configurations

    def generate_command(self, scan, destination: Path, config: str) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Parameters
        ----------
        scan : ~django_mri.models.scan.Scan
            Input scan
        destination : Path
            Output files destination direcotry
        config : str
            Configuration arguments for the command

        Returns
        -------
        str
            Complete execution command
        """

        output_path = destination / self.DEFAULT_OUTPUT_NAME
        command = f"dwifslpreproc {scan.path} {output_path} {config}"
        return command + "".join(
            [
                f" -{key}"
                if key in self.FLAGS and value
                else f" -{key} {value}"
                for key, value in self.configuration.items()
            ]
        )

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

        output_dict = {
            "corrected_image": destination / self.DEFAULT_OUTPUT_NAME,
        }
        for key, value in self.EDDY_OUTPUTS.items():
            output_dict[key] = destination / value
        return output_dict

    def run(self, scan, destination: Path = None) -> dict:
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

        destination = Path(destination) if destination else scan.path.parent
        config = self.add_supplementary_outputs(destination)
        command = self.generate_command(scan, destination, config).split()
        process = subprocess.run(command, capture_output=True)
        if process.returncode:
            raise RuntimeError("Failed to run dwifslpreproc!")
        return self.generate_output_dict(destination)
