"""
Definition of the
:class:`~django_mri.analysis.interfaces.matlab.spm.utils.nifti_validator.NiftiValidator`
class.
"""

from pathlib import Path


class NiftiValidator:
    """
    A utility class used to validate *.nii* inputs and uncompress them if
    necessary.
    """

    def __init__(self, allow_gz: bool = False):
        """
        Class initialization.

        Parameters
        ----------
        allow_gz : bool, optional
            Whether to allow compressed (*.nii.gz*) files, by default False
        """

        self.allow_gz = allow_gz

    def validate_and_fix(self, path: Path) -> Path:
        """
        Validates the provided path represents a *.nii* file and uncompresses
        it if necessary.

        Parameters
        ----------
        path : Path
            *.nii* file path

        Returns
        -------
        Path
            *.nii* file path

        Raises
        ------
        ValueError
            Invalid suffix (not *.nii*)
        FileNotFoundError
            File does not exist
        """

        if isinstance(path, str):
            path = Path(path)
        if not self.validate_extension(path):
            valid_extensions = ".nii or .nii.gz" if self.allow_gz else ".nii"
            raise ValueError(
                f"Input file must have a {valid_extensions} suffix!"
            )
        if not path.is_file():
            raise FileNotFoundError(f"{path} does not exist!")
        return path

    def validate_extension(self, path: Path) -> bool:
        """
        Validate the given file's extension.

        Parameters
        ----------
        path : Path
            File path to check

        Returns
        -------
        bool
            Valid or invalid
        """

        if path.suffix != ".nii":
            if not (self.allow_gz and path.name.endswith(".nii.gz")):
                return False
        return True
