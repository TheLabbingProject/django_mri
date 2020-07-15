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

    __version__ = "BETA"

    def __init__(self, configuration: dict):
        self.configuration = configuration

    def add_supplementary_outputs(self, destination: Path) -> str:
        config = self.configuration.copy()
        for key in self.SUPPLEMENTARY_OUTPUTS:
            if key not in config.keys():
                config[key] = destination
        return config

    def generate_command(self, scan, destination: Path):
        output_path = destination / self.DEFAULT_OUTPUT_NAME
        command = f"dwifslpreproc {scan.path} {output_path} "
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
            "eddyqc_text": destination / "replace_with_true_name.txt",
        }

    def run(self, scan, destination: Path = None) -> dict:
        destination = Path(destination) if destination else scan.path.parent
        config = self.add_supplementary_outputs(destination)
        command = self.generate_command(scan, destination).split()
        process = subprocess.run(command, capture_output=True)
        if process.returncode:
            raise RuntimeError("Failed to run dwifslpreproc!")
        return self.generate_output_dict(destination)
