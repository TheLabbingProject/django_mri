"""
Definition of the :class:`QsiPrep` interface.
"""
import os
from pathlib import Path
from typing import Iterable, Tuple, Union

from django.conf import settings
from django_mri.analysis.interfaces.qsiprep.messages import (
    FS_LICENSE_MISSING, RUN_FAILURE)
from django_mri.analysis.interfaces.qsiprep.utils import (COMMAND, FLAGS,
                                                          FREESURFER_HOME,
                                                          OUTPUTS)
from django_mri.utils import get_singularity_root
from django_mri.utils.utils import get_bids_dir


class QsiPrep:
    """
    An interface for the *qsiprep* preprocessing pipeline.

    References
    ----------
    * qsiprep_

    .. _fmriprep:
       https://qsiprep.readthedocs.io/en/latest/
    """

    #: Binary configurations.
    FLAGS = FLAGS

    #: Expected outputs.
    OUTPUTS = OUTPUTS

    #: Default FreeSurfer home directory.
    DEFAULT_FREESURFER_HOME: Path = Path(FREESURFER_HOME)

    #: QsiPrep output pattern.
    QSIPREP_OUTPUT_PATTERN: str = (
        "{main_dir}/**/{sub_dir}/sub-{subject_id}_{session_id}_{output_id}"
    )

    #: FreeSurfer output pattern.
    FS_OUTPUT_PATTERN: str = "{main_dir}/**/*{output_id}"

    #: Session results pattern.
    SESSION_PATTERN: str = "qsiprep/sub-{subject_id}/ses-*"

    __version__ = None

    def __init__(
        self,
        analysis_root: Union[Path, str] = None,
        **kwargs,
    ):
        """
        Initializes a new :class:`FmriPrep` interface instance.
        """
        self.analysis_root = self.set_output_root(analysis_root)
        self.destination = self.analysis_root / kwargs.pop("destination")
        self.configuration = kwargs
        self.bids_root = self.set_input_root()

    def set_input_root(self) -> Path:
        """
        Query input configuration for a study id,
        if it exists - bids root will be set to the study's.
        Otherwise, it will be set to the database's.

        Returns
        -------
        Path
            Path to a BIDS-valid directory.
        """
        from research.models.study import Study

        study_id = self.configuration.pop("study_id")
        try:
            study = Study.objects.get(id=study_id)
        except Study.DoesNotExist:
            return get_bids_dir()
        else:
            return study.data_directory

    def set_output_root(
        self,
        analysis_root: Union[Path, str] = None,
    ) -> Tuple[Path, Path]:
        """
        Sets the input and output directories to be mounted by singularity

        Returns
        -------
        Tuple[Path, Path]
            Paths to input and output directories, accordingly
        """
        from django_mri.utils import get_mri_root

        mri_root = get_mri_root()
        if not analysis_root:
            analysis_root = mri_root.parent / "analysis"
        return analysis_root

    def find_fs_license(self) -> Path:
        """
        Returns the provided or located FreeSurfer license path.

        Returns
        -------
        Path
            Path to FreeSurfer license file

        Raises
        ------
        FileNotFoundError
            No FreeSurfer license file could be found
        """
        try:
            return self.configuration.pop("fs-license-file")
        except KeyError:
            fs_home = os.getenv("FREESURFER_HOME", self.DEFAULT_FREESURFER_HOME)
            license_file = Path(fs_home) / "license.txt"
            if license_file.exists():
                return license_file
            else:
                raise FileNotFoundError(FS_LICENSE_MISSING)

    def set_configuration_by_keys(self):
        """
        Builds command for qsiprep CLI (via singularity) based on user's
        specifications.

        Returns
        -------
        str
            CLI-compatible command
        """
        key_command = ""
        for key, value in self.configuration.items():
            key_addition = f" --{key}"
            if isinstance(value, list):
                for val in value:
                    key_addition += f" {val}"
            elif key in self.FLAGS and value:
                pass
            else:
                key_addition += f" {value}"
            key_command += key_addition
        return key_command

    def generate_command(self) -> str:
        """
        Returns the command to be executed in order to run the analysis.

        Returns
        -------
        str
            Complete execution command
        """
        fs_license = self.find_fs_license()
        analysis_level = self.configuration.pop("analysis_level")

        singularity_image_root = get_singularity_root()
        command = COMMAND.format(
            bids_origin=str(get_bids_dir()),
            bids_root=self.bids_root,
            destination_parent=self.destination.parent,
            destination_name=self.destination.name,
            analysis_level=analysis_level,
            freesurfer_license=fs_license,
            version=self.__version__,
            security_options=self.security_options,
            singularity_image_root=singularity_image_root,
        )
        return command + self.set_configuration_by_keys()

    def get_security_options(self) -> str:
        options = getattr(settings, "SINGULARITY_SECURITY_OPTIONS", "")
        if options:
            return f'--security="{options}"'
        return ""

    def generate_fs_outputs(self, main_dir: str, output_id: str) -> Iterable[Path]:
        """
        Generate FreeSurfer output paths.

        Parameters
        ----------
        main_dir : str
            Main output directory
        output_id : str
            Output file name pattern

        Yields
        -------
        Path

        """
        pattern = self.FS_OUTPUT_PATTERN.format(main_dir=main_dir, output_id=output_id)
        return self.destination.rglob(pattern)

    def generate_qsiprep_outputs(
        self,
        main_dir: str,
        sub_dir: str,
        subject_id: str,
        session_id: str,
        output_id: str,
    ) -> Iterable[Path]:
        """
        Generate qsiprep output paths.

        Parameters
        ----------
        main_dir : str
            Main output directory
        sub_dir : str
            Results sub-directory name
        subject_id : str
            String subject ID
        session_id : str
            String session ID
        output_id : str
            Output file name pattern

        Yields
        -------
        Path
            Output paths
        """
        pattern = self.QSIPREP_OUTPUT_PATTERN.format(
            main_dir=main_dir,
            sub_dir=sub_dir,
            subject_id=subject_id,
            session_id=session_id,
            output_id=output_id,
        )
        return self.destination.rglob(pattern)

    def find_output(self, partial_output: str, subject_id: str, session_id: str):
        """
        uses the destination and some default dictionary to locate specific
        output files of *qsiprep*.

        Parameters
        ----------
        partial_output : str
            A string that identifies a specific output
        subject_id : str
            Subject string ID
        session_id : str
            Session string ID
        """
        main_dir, sub_dir, output_id = self.OUTPUTS.get(partial_output)
        if main_dir == "freesurfer":
            outputs = list(self.generate_fs_outputs(main_dir, output_id))
        elif main_dir == "qsiprep":
            outputs = list(
                self.generate_qsiprep_outputs(
                    main_dir, sub_dir, subject_id, session_id, output_id
                )
            )
        # if len(outputs) == 1:
        #     return str(outputs[0])
        # elif len(outputs) > 1:
        if "native" in partial_output:
            return [str(f) for f in outputs if ("MNI" not in f.name)]
        return [str(f) for f in outputs]

    def generate_output_dict(self) -> dict:
        """
        Generates a dictionary of the expected output file paths by key.

        Returns
        -------
        dict
            Output files by key
        """
        output_dict = {}
        subject_ids = self.configuration.get("participant_label")
        for subject_id in subject_ids:
            output_dict[subject_id] = {}
            # session_pattern = self.SESSION_PATTERN.format(
            #     subject_id=subject_id
            # )
            for key in self.OUTPUTS:
                output_dict[subject_id][key] = self.find_output(key, subject_id, "*")
        if len(output_dict) == 1:
            return output_dict.get(subject_id)
        return output_dict

    def run(self) -> dict:
        """
        Runs *qsiprep* with the provided *bids_dir* as input.
        If *destination* is not specified, output files will be created within
        *bids_dir*\'s parent directory.

        Returns
        -------
        dict
            Dictionary with keys and values corresponding to descriptions and
            files of *fmriprep*\'s outputs accordingly

        Raises
        ------
        RuntimeError
            In case of failed execution, raises an appropriate error
        """
        command = self.generate_command()
        raised_exception = os.system(command)
        if raised_exception:
            message = RUN_FAILURE.format(command=command, exception=raised_exception)
            raise RuntimeError(message)
        return self.generate_output_dict()

    @property
    def security_options(self) -> str:
        return self.get_security_options()


class QsiPrep0143(QsiPrep):
    __version__ = "0.14.3"


class QsiPrep0160RC3(QsiPrep):
    __version__ = "0.16.0RC3"
