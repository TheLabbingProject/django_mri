"""
Definition of the
:class:`django_mri.analysis.interfaces.matlab.spm.spm_procedure.SPMProcedure`
class.
"""

import shutil

from django_mri.analysis.interfaces.matlab.spm.utils.batch_templates import (
    TEMPLATES,
)
from pathlib import Path


class SPMProcedure:
    """
    General base class for SPM procedure (i.e. function) interfaces.
    """

    #: Key of the batch template path in the
    #: :attr:`~django_mri.analysis.interfaces.matlab.spm.utils.batch_templates
    # .TEMPLATES` dictionary.
    BATCH_TEMPLATE_ID = ""

    #: Default name for the created batch file.
    DEFAULT_BATCH_FILE_NAME = ""

    #: Default configuration options.
    DEFAULTS = {}

    #: A dictionary containing the paths of the expected output files by key.
    OUTPUT_DEFINITIONS = {}

    #: Artifacts created during run execution.
    AUXILIARY_OUTPUT = {}

    def __init__(self, **kwargs):
        """
        Initialized the class, including any options (specified as keyword
        arguments) in the
        :attr:`~django_mri.analysis.interfaces.matlab.spm.spm_procedure.SPMProcedure.options`
        attribute.
        """

        self.options = {**self.DEFAULTS, **kwargs}
        self.engine = self.start_matlab_engine()
        self.spm_directory = self.get_spm_directory()

    @classmethod
    def start_matlab_engine(cls):
        import matlab.engine

        return matlab.engine.start_matlab()

    def get_spm_directory(self) -> Path:
        spm_script = self.engine.which("spm")
        if spm_script:
            return Path(spm_script).parent
        raise RuntimeError("Failed to find local SPM installation!")

    def get_batch_template_path(self) -> Path:
        try:
            return TEMPLATES[self.BATCH_TEMPLATE_ID]
        except KeyError:
            raise NotImplementedError(
                f"No batch template for {self.BATCH_TEMPLATE_ID} located!"
            )

    def read_batch_template(self) -> str:
        template_path = self.get_batch_template_path()
        with open(template_path, "r") as template:
            return template.read()

    def update_batch_template(self, *args, **kwrags) -> str:
        raise NotImplementedError(
            "The `update_batch_template` method is not implemented!"
        )

    def save_batch(self, batch: str, destination: Path):
        with open(destination, "w") as batch_file:
            batch_file.write(batch)

    def create_batch_file(
        self, data_path: Path, file_destination: Path = None
    ) -> str:
        batch = self.update_batch_template(data_path)
        destination = file_destination or data_path.with_name(
            self.DEFAULT_BATCH_FILE_NAME
        )
        self.save_batch(batch, destination)
        return destination

    def run(self, *args, **kwargs) -> dict:
        raise NotImplementedError("The `run` method is not implemented!")

    def format_string_output_definition(
        self, input_path: Path, value: str
    ) -> Path:
        file_name = input_path.with_suffix("").name
        return input_path.parent / value.format(file_name=file_name)

    def format_list_output_definition(
        self, input_path: Path, value: list
    ) -> list:
        file_name = input_path.with_suffix("").name
        return [
            input_path.parent / element.format(file_name=file_name)
            for element in value
        ]

    def format_dict_output_definition(
        self, input_path: Path, key: str, value: dict
    ):
        selected_option = self.options.get(key)
        output_definition = value.get(selected_option)
        if isinstance(output_definition, str):
            return self.format_string_output_definition(
                input_path, output_definition
            )
        elif isinstance(output_definition, list):
            return self.format_list_output_definition(
                input_path, output_definition
            )

    def format_output_definition(self, input_path: Path, key: str, value):
        if isinstance(value, str):
            return self.format_string_output_definition(input_path, value)
        elif isinstance(value, list):
            return self.format_list_output_definition(input_path, value)
        elif isinstance(value, dict):
            return self.format_dict_output_definition(input_path, key, value)

    def create_output_dict(self, input_path: Path) -> dict:
        result = {}
        generated_output = {
            key: value
            for key, value in self.OUTPUT_DEFINITIONS.items()
            if self.options.get(key)
        }
        generated_output.update(self.AUXILIARY_OUTPUT)
        for key, value in generated_output.items():
            formatted_value = self.format_output_definition(
                input_path, key, value
            )
            if formatted_value:
                result[key] = formatted_value
        return result

    def move_output_file(
        self, path: Path, run_dir: Path, destination_dir: Path
    ) -> dict:
        destination = Path(destination_dir) / Path(path).relative_to(run_dir)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(destination))
        if not len(list(path.parent.iterdir())):
            path.parent.rmdir()
        return destination

    def move_output_files(self, origin, run_dir: Path, destination: Path):
        if isinstance(origin, Path):
            return self.move_output_file(origin, run_dir, destination)
        else:
            return [
                self.move_output_file(element, run_dir, destination)
                for element in origin
            ]

    def move_output(
        self, output_dict: dict, run_dir: Path, destination: Path
    ) -> dict:
        return {
            key: self.move_output_files(value, run_dir, destination)
            for key, value in output_dict.items()
        }
