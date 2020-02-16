from django_mri.analysis.matlab.spm.cat12.segmentation.defaults import (
    SEGMENTATION_DEFAULTS,
)
from django_mri.analysis.matlab.spm.cat12.segmentation.outputs import (
    SEGMENTATION_OUTPUT,
    AUXILIARY_OUTPUT,
)
from django_mri.analysis.matlab.spm.cat12.segmentation.utils import (
    verbosify_output_dict,
)
from django_mri.analysis.matlab.spm.cat12.utils.template_files import (
    RELATIVE_DARTEL_TEMPLATE_LOCATION,
    RELATIVE_TISSUE_PROBABILITY_MAP_LOCATION,
)
from django_mri.analysis.matlab.spm.cat12.segmentation.transformations import (
    SEGMENTATION_TRANSFORMATIONS,
)
from django_mri.analysis.matlab.spm.spm_procedure import SPMProcedure
from django_mri.analysis.matlab.spm.utils.nifti_validator import NiftiValidator
from django_mri.utils.compression import uncompress

from pathlib import Path


class Segmentation(SPMProcedure):
    BATCH_TEMPLATE_ID = "CAT12 Segmentation"
    DEFAULT_BATCH_FILE_NAME = "segmentation.m"
    TRANSFORMATIONS = SEGMENTATION_TRANSFORMATIONS
    DEFAULTS = SEGMENTATION_DEFAULTS
    OUTPUT_DEFINITIONS = SEGMENTATION_OUTPUT
    AUXILIARY_OUTPUT = AUXILIARY_OUTPUT
    REDUNDANT_LOG_PATTERN = "catlog_main_*_log*.txt"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nifti_validator = NiftiValidator(allow_gz=True)
        self.tissue_probability_map_path = (
            self.spm_directory / RELATIVE_TISSUE_PROBABILITY_MAP_LOCATION
        )
        self.dartel_template_path = (
            self.spm_directory / RELATIVE_DARTEL_TEMPLATE_LOCATION
        )

    def transform_options(self) -> dict:
        transformed = {}
        for key, value in self.options.items():
            transformation = self.TRANSFORMATIONS.get(key, {})
            value = transformation.get(value, value)
            transformed[key] = int(value) if isinstance(value, bool) else value
        return transformed

    def update_batch_template(self, data_path: Path) -> str:
        batch = self.read_batch_template()
        options = self.transform_options()
        batch = batch.replace("$DATA_PATH", str(data_path))
        batch = batch.replace("$TPM_PATH", str(self.tissue_probability_map_path))
        batch = batch.replace("$DARTEL_TEMPLATE_PATH", str(self.dartel_template_path))
        for key, value in options.items():
            batch = batch.replace(f"${key.upper()}", str(value))
        return batch

    def validate_and_fix_input_data(self, path: Path) -> tuple:
        path = self.nifti_validator.validate_and_fix(path)

        # If the input is zipped, check for an existing unzipped version or create one
        if path.suffix == ".gz":
            # In case un unzipped version exists already, return the unzipped version
            # and 'False' for having created it
            if path.with_suffix("").is_file():
                return path.with_suffix(""), False

            # Otherwise, create an unzipped version and return 'True' for having created it
            return uncompress(path), True
        return path, False

    def remove_redundant_logs(self, run_dir: Path):
        for log in run_dir.glob(self.REDUNDANT_LOG_PATTERN):
            log.unlink()

    def organize_output(
        self,
        path: Path,
        created_uncompressed_version: bool,
        destination: Path,
        remove_redundant_logs: bool,
        verbose_output_dict: bool = False,
    ) -> dict:
        if remove_redundant_logs:
            self.remove_redundant_logs(path.parent)
        if created_uncompressed_version:
            path.unlink()
        output_dict = self.create_output_dict(path)
        if destination:
            output_dict = self.move_output(
                output_dict=output_dict, run_dir=path.parent, destination=destination
            )
        if verbose_output_dict:
            return verbosify_output_dict(output_dict)
        return output_dict

    def run(
        self,
        path: Path,
        destination: Path = None,
        remove_redundant_logs: bool = True,
        verbose_output_dict: bool = False,
    ) -> dict:
        path, created_uncompressed_version = self.validate_and_fix_input_data(path)
        batch_file = self.create_batch_file(path)
        self.engine.run(str(batch_file), nargout=0)
        return self.organize_output(
            path,
            created_uncompressed_version,
            destination,
            remove_redundant_logs,
            verbose_output_dict,
        )

