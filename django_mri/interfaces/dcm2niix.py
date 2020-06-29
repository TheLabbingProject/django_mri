import os
import subprocess
import glob
from pathlib import Path
import re
import warnings

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
            path, destination, compressed=compressed, generate_json=generate_json,
        )
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            returned_path = self.extract_output_path(str(stdout), compressed)
            expected_file = destination.with_suffix(".nii.gz")
            if returned_path != expected_file:
                warnings.warn(
                    "Returned NIfTI path does not match expected destination.\nThis could indicate a problem with the conversion."
                )
            if Path(str(returned_path)).is_file():
                return returned_path
            else:
                print(returned_path)
                raise RuntimeError(
                    "Failed to create NIfTI file using dcm2niix! Please check application configuration"
                )

        except FileNotFoundError:
            raise NotImplementedError(
                "Could not call dcm2niix! Please check settings configuration."
            )

    def extract_output_path(self, stdout: str, compressed: bool) -> Path:
        try:
            path = re.findall(r"as (\/.*?\.[\w]+)", stdout)[0].split(" (")[0]
        except IndexError:
            return None
        ext = ".nii.gz" if compressed else ".nii"
        return Path(path).with_suffix(ext)
