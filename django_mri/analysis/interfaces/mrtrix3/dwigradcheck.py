"""
Definition of the
:class:`~django_mri.analysis.interfaces.mrtrix3.dwigradcheck` interface.
"""

import os
from pathlib import Path


class DwiGradCheck:
    """
    An interface for the MRtrix3 *dwigradcheck* script.

    References
    ----------
    * dwigradcheck_

    .. mrcat:
       https://mrtrix.readthedocs.io/en/latest/reference/commands/dwigradcheck.html
    """

    #: "Flags" indicate parameters that are specified without any arguments,
    #: i.e. they are a switch for some binary configuration.
    FLAGS = (
        "force",
        "quiet",
        "info",
        "nocleanup",
    )
    MRTRIX_GRAD_OUTPUT = {"export_grad_mrtrix": "dwi.b"}
    FSL_GRAD_OUTPUT = {"export_grad_fsl": ["dwi.bvec", "dwi.bval"]}

    #: Irrelevant inputs that needs to be removed.
    IRRELEVANT_INPUTS = ["export_fsl_bvec", "export_fsl_bval"]

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
            elif key in self.FLAGS or key in self.IRRELEVANT_INPUTS:
                key_addition = ""
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def fix_output_configuration(self, config: dict, destination: Path):
        fsl_export = "export_fsl_bvec" in config and "export_fsl_bval" in config
        mrtrix_export = "export_grad_mrtrix" in config
        if fsl_export and mrtrix_export:
            raise RuntimeError(
                "You cannot use more than one of the following options: -export_grad_mrtrix, -export_grad_fsl"
            )
        elif fsl_export:
            bvec_path = config.pop("export_fsl_bvec")
            bval_path = config.pop("export_fsl_bval")
            config["export_grad_fsl"] = f"{bvec_path} {bval_path}"
        elif not mrtrix_export:
            bvec_path = destination / "dwi.bvec"
            bval_path = destination / "dwi.bval"
            config["export_grad_fsl"] = f"{bvec_path} {bval_path}"
        return config

    def generate_command(self, config: dict) -> str:
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

        return f"dwigradcheck" + f" {in_file}" + self.set_configuration_by_keys(config)

    def generate_output_dict(self, config: dict, destination: Path) -> dict:
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
        export_grad_fsl = config.get("export_grad_fsl")
        export_grad_mrtrix = config.get("export_grad_mrtrix")
        if export_grad_fsl:
            (
                output_dict["grad_fsl_bvec"],
                output_dict["grad_fsl_bval"],
            ) = export_grad_fsl.split(" ")
        elif export_grad_mrtrix:
            output_dict["grad_mrtrix"] = export_grad_mrtrix
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
        destination = Path(self.configuration.get("export_fsl_bvec")).parent
        config = self.fix_output_configuration(self.configuration, destination)
        command = self.generate_command(config)
        raise_exception = os.system(command)
        if raise_exception:
            raise RuntimeError(
                f"Failed to run dwigradcheck!\nExecuted command: {command}"
            )
        return self.generate_output_dict(config, destination)
