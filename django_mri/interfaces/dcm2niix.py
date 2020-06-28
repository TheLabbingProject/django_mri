import os
import subprocess
import glob
from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent
DCM2NIIX = BASE_DIR / "utils" / "dcm2niix"


class Dcm2niix:
    FLAGS = {"compressed": "-z", "BIDS": "-b", "name": "-f", "directory": "-o"}
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
        command = self.generate_command(
            path,
            destination,
            compressed=compressed,
            generate_json=generate_json,
        )
        try:
            subprocess.check_output(command)
            expected_file = destination.with_suffix(".nii.gz")
            if expected_file.is_file():
                return expected_file
            else:
                raise RuntimeError(
                    "Failed to create NIfTI file using dcm2niix! Please check application configuration"
                )

        except FileNotFoundError:
            raise NotImplementedError(
                "Could not call dcm2niix! Please check settings configuration."
            )
