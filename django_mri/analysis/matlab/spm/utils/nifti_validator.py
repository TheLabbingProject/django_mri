from pathlib import Path


class NiftiValidator:
    def __init__(self, allow_gz: bool = False):
        self.allow_gz = allow_gz

    def validate_and_fix(self, path: Path):
        if isinstance(path, str):
            path = Path(path)
        if not self.validate_extension(path):
            valid_extensions = ".nii or .nii.gz" if self.allow_gz else ".nii"
            raise ValueError(f"Input file must have a {valid_extensions} suffix!")
        if not path.is_file():
            raise FileNotFoundError(f"{path} does not exist!")
        return path

    def validate_extension(self, path: Path) -> bool:
        if path.suffix != ".nii":
            if not (self.allow_gz and path.name.endswith(".nii.gz")):
                return False
        return True

