import subprocess

from pathlib import Path


class DwiFslPreproc:
    FLAGS = (
        "align_seepi",
        "rpe_none",
        "rpe_pair",
        "rpe_all",
        "rpe_header",
        "force",
        "quiet",
        "info",
        "nocleanup",
    )
    SUPPLEMENTARY_OUTPUTS = ("eddyqc_text", "eddyqc_all")
    DEFAULT_OUTPUT_NAME = "preprocessed_dwi.mif"
    EDDY_OUTPUTS = {
        "out_movement_rms": "eddy_movement_rms",
        "eddy_mask": "eddy_mask.nii",
        "out_outlier_map": "eddy_outlier_map",
        "out_outlier_n_sqr_stdev_map": "eddy_outlier_n_sqr_stdev_map",
        "out_outlier_n_stdev_map": "eddy_outlier_n_stdev_map",
        "out_outlier_report": "eddy_outlier_report",
        "out_parameter": "eddy_parameters",
        "out_restricted_movement_rms": "eddy_restricted_movement_rms",
        "out_shell_alignment_parameters": "eddy_post_eddy_shell_alignment_parameters",
        "out_shell_pe_translation_parameters": "eddy_post_eddy_shell_PE_translation_parameters",
    }
    __version__ = "BETA"

    def __init__(self, configuration: dict):
        self.configuration = configuration

    def add_supplementary_outputs(self, destination: Path) -> str:
        config = self.configuration.copy()
        for key in self.SUPPLEMENTARY_OUTPUTS:
            if key not in config.keys():
                config[key] = destination
        return config

    def generate_command(self, scan, destination: Path, config: str):
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

    def generate_output_dict(self, destination: Path):
        output_dict = {
            "corrected_image": destination / self.DEFAULT_OUTPUT_NAME,
        }
        for key, value in self.EDDY_OUTPUTS.items():
            output_dict[key] = destination / value
        return output_dict

    def run(self, scan, destination: Path = None) -> dict:
        destination = Path(destination) if destination else scan.path.parent
        config = self.add_supplementary_outputs(destination)
        command = self.generate_command(scan, destination, config).split()
        process = subprocess.run(command, capture_output=True)
        if process.returncode:
            raise RuntimeError("Failed to run dwifslpreproc!")
        return self.generate_output_dict(destination)
