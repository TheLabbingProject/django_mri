"""
Definition of the :class:`LongitudinalSegmentation` class.
"""

from pathlib import Path
from typing import List, Tuple

from django_mri.analysis.interfaces.matlab.spm.cat12.longitudinal_segmentation.defaults import \
    LONGITUDINAL_SEGMENTATION_DEFAULTS  # noqa: E501
from django_mri.analysis.interfaces.matlab.spm.cat12.longitudinal_segmentation.outputs import (  # noqa: E501
    AUXILIARY_OUTPUT, LONGITUDINAL_SEGMENTATION_OUTPUT)
from django_mri.analysis.interfaces.matlab.spm.cat12.longitudinal_segmentation.transformations import \
    LONGITUDINAL_SEGMENTATION_TRANSFORMATIONS  # noqa: E501
from django_mri.analysis.interfaces.matlab.spm.cat12.longitudinal_segmentation.utils import \
    verbosify_output_dict  # noqa: E501
from django_mri.analysis.interfaces.matlab.spm.cat12.utils.template_files import (  # noqa: E501
    RELATIVE_SHOOTING_TISSUE_PROBABILITY_MAP_LOCATION,
    RELATIVE_TISSUE_PROBABILITY_MAP_LOCATION)
from django_mri.analysis.interfaces.matlab.spm.spm_procedure import \
    SPMProcedure
from django_mri.analysis.interfaces.matlab.spm.utils.nifti_validator import \
    NiftiValidator
from django_mri.utils.compression import uncompress


class LongitudinalSegmentation(SPMProcedure):
    """
    An interface for the CAT12 longitudinal segmentation function.
    """

    BATCH_TEMPLATE_ID = "CAT12 Longitudinal Segmentation"
    DEFAULT_BATCH_FILE_NAME = "longitudinal_segmentation.m"
    TRANSFORMATIONS = LONGITUDINAL_SEGMENTATION_TRANSFORMATIONS
    DEFAULTS = LONGITUDINAL_SEGMENTATION_DEFAULTS
    OUTPUT_DEFINITIONS = LONGITUDINAL_SEGMENTATION_OUTPUT
    AUXILIARY_OUTPUT = AUXILIARY_OUTPUT
    REDUNDANT_LOG_PATTERN = "catlog_main_*_log*.txt"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nifti_validator = NiftiValidator(allow_gz=True)
        self.tissue_probability_map_path = (
            self.spm_directory / RELATIVE_TISSUE_PROBABILITY_MAP_LOCATION
        )
        self.shooting_tpm_path = (
            self.spm_directory
            / RELATIVE_SHOOTING_TISSUE_PROBABILITY_MAP_LOCATION
        )

    def transform_options(self) -> dict:
        """
        Apply any transformation defined in the
        :mod:`~django_mri.analysis.interfaces.matlab.spm.cat12.longitudinal_segmentation.transformations`
        module to the
        :attr:`~django_mri.analysis.interfaces.matlab.spm.spm_procedure.SPMProcedure.options`
        dictionary.

        Returns
        -------
        dict
            Tranformed options dictionary
        """

        transformed = {}
        for key, value in self.options.items():
            transformation = self.TRANSFORMATIONS.get(key, {})
            value = transformation.get(value, value)
            transformed[key] = int(value) if isinstance(value, bool) else value
        return transformed

    def update_batch_template(self, scans: List[Path]) -> str:
        """
        Returns a copy of the batch template, updated with the configured
        options and scan paths.

        Parameters
        ----------
        scans : List[Path]
            Paths of the input *.nii* files

        Returns
        -------
        str
            Updated batch template
        """

        batch = self.read_batch_template()
        options = self.transform_options()
        t1w_scans = [f"'{scan.nifti.uncompressed},1'" for scan in scans]
        t1w_scans = "\n".join(t1w_scans)
        batch = batch.replace("$T1W_SCANS", t1w_scans)
        batch = batch.replace(
            "$TPM_PATH", str(self.tissue_probability_map_path)
        )
        batch = batch.replace(
            "$SHOOTING_TPM_PATH", str(self.shooting_tpm_path)
        )
        for key, value in options.items():
            batch = batch.replace(f"${key.upper()}", str(value))
        return batch

    def validate_and_fix_input_data(self, scans: List[Path]) -> List[Path]:
        """
        Validate the provided data path and creates an unzipped version if
        required.

        Parameters
        ----------
        path : List[Path]
            List of T1-weighted scan paths

        Returns
        -------
        List[tuple]
            List of tuples with shape (path string, created)
        """

        scans = [self.nifti_validator.validate_and_fix(path) for path in scans]

        results = []
        for path in scans:
            # If the input is zipped, check for an existing unzipped version or
            # create one.
            if path.suffix == ".gz":
                # In case un unzipped version exists already, return the
                # unzipped version and 'False' for having created it.
                if path.with_suffix("").is_file():
                    results.append((path.with_suffix(""), False))
                # Otherwise, create an unzipped version and return 'True' for
                # having created it.
                results.append(uncompress(path), True)
            else:
                results.append((path, False))
        return results

    def remove_redundant_logs(self, run_dir: Path):
        """
        Removed unnecessary logs created during execution.

        Parameters
        ----------
        run_dir : Path
            Output files destination
        """

        for log in run_dir.glob(self.REDUNDANT_LOG_PATTERN):
            log.unlink()

    def organize_output(
        self,
        scans: List[str],
        created_uncompressed_version: List[bool],
        destination: Path,
        remove_redundant_logs: bool,
        verbose_output_dict: bool = False,
    ) -> dict:
        """
        Organized output files after execution.

        Parameters
        ----------
        path : Path
            Input file path
        destination : Path
            Output files destination directory
        created_uncompressed_version : List[bool]
            List of boolean values signaling whether a .nii version was created
            for the purposes of this run and should be removed
        remove_redundant_logs : bool
            Whether to remove logs created during execution or not
        verbose_output_dict : bool, optional
            Whether to flatten the output dictionary to facilitate integration
            with django_analyses, by default False

        Returns
        -------
        dict
            Output files by keys
        """

        # TODO:
        #   * Find out if there are created logs and what is the run dir if different directories and fix
        #     remove_redundant_long, create_output_dict, and move_output accordingly
        if remove_redundant_logs:
            self.remove_redundant_logs(path.parent)
        for i, created in enumerate(created_uncompressed_version):
            if created:
                Path(scans[i]).unlink()
        output_dict = self.create_output_dict(scans)
        if destination:
            output_dict = self.move_output(
                output_dict=output_dict,
                run_dir=path.parent,
                destination=destination,
            )
        if verbose_output_dict:
            return verbosify_output_dict(output_dict)
        return output_dict

    def run(
        self,
        scans: List[Path],
        destination: Path = None,
        remove_redundant_logs: bool = True,
        verbose_output_dict: bool = False,
    ) -> dict:
        """
        Run CAT12 longitudinal segmentation with the provided *.nii* input
        files.

        Parameters
        ----------
        scans : List[Path]
            Single subject's T1-weighted scans from different time-points
        destination : Path, optional
            Output file destination directory, by default None
        remove_redundant_logs : bool, optional
            Whether to remove some logs created during execution, by default
            True
        verbose_output_dict : bool, optional
            Whether to verbosify and flatten the output files dictionary, by
            default False

        Returns
        -------
        dict
            Output files by key
        """

        scans, created = zip(*self.validate_and_fix_input_data(scans))
        batch_file = self.create_batch_file(scans)
        self.engine.run(str(batch_file), nargout=0)
        return self.organize_output(
            scans,
            created,
            destination,
            remove_redundant_logs,
            verbose_output_dict,
        )

