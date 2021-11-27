"""
Definition of the :class:`Scan` model.
"""
import logging
import warnings
from pathlib import Path
from typing import Any, Dict, List, Union

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import IntegrityError, models
from django_analyses.models.input import (DirectoryInput, FileInput, Input,
                                          ListInput)
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel
from django_mri.analysis.interfaces.dcm2niix import Dcm2niix
from django_mri.models import help_text, messages
from django_mri.models.managers.scan import ScanQuerySet
from django_mri.models.messages import SCAN_UPDATE_NO_DICOM
from django_mri.models.nifti import NIfTI
from django_mri.utils.bids import BidsManager
from django_mri.utils.utils import (get_bids_manager, get_group_model,
                                    get_mri_root)
from nilearn.image import mean_img
from nilearn.plotting import cm, view_img

FLAG_3D = "mprage", "spgr", "flair", "t1", "t2"
FLAG_4D = "fmri", "dmri"


class Scan(TimeStampedModel):
    """
    A model used to represent an MRI scan independently from the file-format in
    which it is saved. This model handles any conversions between formats in
    case they are required, and allows for easy querying of MRI scans based on
    universal attributes.
    """

    #: The institution in which this scan was acquired.
    institution_name = models.CharField(max_length=64, blank=True, null=True)

    #: Acquisition datetime.
    time = models.DateTimeField(
        blank=True, null=True, help_text=help_text.SCAN_TIME
    )

    #: Short description of the scan's acquisition parameters.
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=help_text.SCAN_DESCRIPTION,
    )

    #: The relative number of this scan in the session in which it was
    #: acquired.
    number = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_NUMBER,
    )

    #: The time between the application of the radio-frequency excitation pulse
    #: and the peak of the signal induced in the coil (in milliseconds).
    echo_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_ECHO_TIME,
    )

    #: The time between two successive RF pulses (in milliseconds).
    repetition_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_REPETITION_TIME,
    )

    #: The time between the 180-degree inversion pulse and the following
    #: spin-echo (SE) sequence (in milliseconds).
    inversion_time = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=help_text.SCAN_INVERSION_TIME,
    )

    #: The spatial resolution of the image in millimeters.
    spatial_resolution = ArrayField(
        models.FloatField(), size=3, blank=True, null=True
    )

    #: Any other comments about this scan.
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=help_text.SCAN_COMMENTS,
    )

    #: If this instance's origin is a DICOM file, or it was saved as one, this
    #: field stores the association with the appropriate
    #: :class`django_dicom.models.series.Series` instance.
    dicom = models.OneToOneField(
        "django_dicom.Series",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="scan",
        verbose_name="DICOM Series",
    )

    #: Keeps track of whether we've updated the instance's fields from DICOM
    #: header data or not.
    is_updated_from_dicom = models.BooleanField(default=False)

    #: If converted to NIfTI, keep a reference to the resulting instance.
    #: The reason it is suffixed with an underline is to allow for "nifti"
    #: to be used as a property that automatically returns an existing instance
    #: or creates one.
    _nifti = models.OneToOneField(
        "django_mri.NIfTI", on_delete=models.SET_NULL, blank=True, null=True
    )

    #: Individual scans may be associated with multiple `Group` instances.
    #: This is meant to provide flexibility in managing access to data between
    #: researchers working on different studies.
    #: The `Group` model is expected to be specified as `STUDY_GROUP_MODEL` in
    #: the project's settings.
    study_groups = models.ManyToManyField(
        get_group_model(), related_name="mri_scan_set", blank=True
    )

    #: Keeps a record of the user that added this scan.
    added_by = models.ForeignKey(
        get_user_model(),
        related_name="mri_uploads",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    #: Associates this scan with some session of a subject.
    session = models.ForeignKey(
        "django_mri.Session", on_delete=models.CASCADE,
    )

    REPRESENTATIONS = (
        "dicom_representation",
        "nifti_representation",
        "mif_representation",
    )
    DERIVATIVE_QUERY = {
        FileInput: "value",
        ListInput: "value__contains",
        DirectoryInput: "value",
    }

    objects = ScanQuerySet.as_manager()

    _bids_manager: BidsManager = None
    _logger = logging.getLogger("data.mri.scan")

    class Meta:
        unique_together = ("number", "session")
        ordering = ("-time",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation of this instance
        """
        formatted_time = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.description} from {formatted_time}"

    def save(self, *args, **kwargs) -> None:
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom validation.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """
        if self.dicom and not self.is_updated_from_dicom:
            self.update_fields_from_dicom()
        super().save(*args, **kwargs)

    def update_fields_from_dicom(self) -> None:
        """
        Sets instance fields from related DICOM series.

        Raises
        ------
        AttributeError
            If not DICOM series is related to this scan
        """
        if self.dicom:
            self.institution_name = self.dicom.institution_name
            self.number = self.dicom.number
            self.time = self.dicom.datetime
            self.description = self.dicom.description
            self.echo_time = self.dicom.echo_time
            self.inversion_time = self.dicom.inversion_time
            self.repetition_time = self.dicom.repetition_time
            self.spatial_resolution = self.dicom.spatial_resolution
            self.is_updated_from_dicom = True
        else:
            message = SCAN_UPDATE_NO_DICOM.format(pk=self.id)
            raise AttributeError(message)

    def infer_sequence_type(self) -> str:
        """
        Tries to infer the sequence type using associated data.

        Returns
        -------
        str
            The inferred sequence type
        """
        if self.dicom:
            return self.dicom.sequence_type

    def get_default_nifti_dir(self) -> Path:
        """
        Returns the default location for the creation of a NIfTI version of the
        scan. Currently only conversion from DICOM is supported.

        Returns
        -------
        str
            Default location for conversion output
        """
        if self.dicom:
            path = str(self.dicom.path).replace("DICOM", "NIfTI")
            return Path(path).parent
        return get_mri_root() / "NIfTI"

    def get_default_nifti_name(self) -> str:
        """
        Returns the default file name for a NIfTI version of this scan.

        Returns
        -------
        str
            Default file name
        """
        return str(self.id)

    def get_default_nifti_destination(self) -> Path:
        """
        Returns the default path for a NIfTI version of this scan.

        Returns
        -------
        str
            Default path for NIfTI file
        """
        directory = self.get_default_nifti_dir()
        name = self.get_default_nifti_name()
        return directory / name

    def dicom_to_nifti(
        self,
        destination: Path = None,
        compressed: bool = True,
        generate_json: bool = True,
        persistent: bool = True,
    ) -> NIfTI:
        """
        Convert this scan from DICOM to NIfTI using _dcm2niix.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Parameters
        ----------
        destination : Path, optional
            The desired path for conversion output (the default is None, which
            will create the file in some default location)

        Raises
        ------
        AttributeError
            If no DICOM series is related to this scan

        Returns
        -------
        NIfTI
            A :class:`django_mri.NIfTI` instance referencing the conversion
            output
        """
        if self.sequence_type == "localizer":
            warnings.warn(messages.NO_LOCALIZER_NIFTI)
        elif self.dicom:
            bids = False
            if destination is None:
                destination = self.bids_manager.build_bids_path(self)
                if destination is None:
                    destination = self.get_default_nifti_destination()
                else:
                    bids = True
            elif not isinstance(destination, Path):
                destination = Path(destination)
            destination.parent.mkdir(exist_ok=True, parents=True)
            try:
                nifti_path = Dcm2niix().convert(
                    self.dicom.path,
                    destination,
                    compressed=compressed,
                    generate_json=generate_json,
                )
            except RuntimeError as e:
                if persistent:
                    warnings.warn(str(e))
                else:
                    raise
            else:
                nifti = NIfTI.objects.create(path=nifti_path, is_raw=True)
                self._nifti = nifti
                self.save()
                if bids:
                    self.bids_manager.postprocess(nifti)
                return nifti
        else:
            message = messages.DICOM_TO_NIFTI_NO_DICOM.format(scan_id=self.id)
            raise AttributeError(message)

    def sync_bids(self, log_level: int = logging.DEBUG):
        self._logger.log(log_level, f"Checking scan #{self.id} BIDS status...")
        mri_root = get_mri_root()
        if self._nifti:
            current_path = Path(self.nifti.path)
            relative_path = current_path.relative_to(mri_root)
            self._logger.log(log_level, f"Current path: {relative_path}")
            suffix = "".join(current_path.suffixes)
            destination = self.bids_manager.build_bids_path(
                self, log_level=log_level
            )
            if destination is not None:
                expected_path = destination.with_suffix(suffix)
                if expected_path != current_path:
                    expected_relative = expected_path.relative_to(mri_root)
                    self._logger.log(
                        log_level, f"Generated BIDS path: {expected_relative}"
                    )
                    self._logger.log(
                        log_level, "Difference found! Renaming file..."
                    )
                    try:
                        self.nifti.rename(expected_path, log_level=log_level)
                    except IntegrityError:
                        existing = NIfTI.objects.get(path=expected_path)
                        if current_path.name.startswith("_"):
                            raise IntegrityError(
                                f"Failed to resolve identical paths for NIfTI instances #{self.nifti.id} and #{existing.id}"  # noqa: E501
                            )
                        self._logger.log(
                            log_level,
                            f"Existing NIfTI instance (#{existing.id}) found at expected path!",  # noqa: E501
                        )
                        self._logger.log(
                            log_level,
                            "Moving existing NIfTI file to temporary path.",
                        )
                        existing_path = Path(existing.path)
                        tmp_destination = existing_path.parent / (
                            "_" + existing_path.name
                        )
                        existing.rename(tmp_destination)
                        self._logger.log(
                            log_level,
                            f"Existing NIfTI successfully moved to {tmp_destination.name}",  # noqa: E501
                        )
                        self.nifti.rename(expected_path, log_level=log_level)
                        existing.scan.sync_bids(log_level=log_level)
                    self._logger.log(
                        log_level,
                        f"Associated NIfTI instance (#{self.nifti.id} successfully moved to {expected_relative}",  # noqa: E501
                    )
            else:
                self._logger.log(
                    log_level,
                    f"Scan #{self.id} ({self.description}) has no BIDS compatible path.",  # noqa: E501
                )
        else:
            self._logger.debug(f"No NIfTI instance found for scan #{self.id}.")

    def warn_subject_mismatch(self, subject):
        """
        Warns the user regarding a mismatch in subject identity.

        Parameters
        ----------
        subject : django.db.models.Model
            Suggested subject identity
        """
        message = messages.SUBJECT_MISMATCH.format(
            scan_id=self.id,
            existing_subject_id=self.session.subject.id,
            assigned_subject_id=subject.id,
        )
        warnings.warn(message)

    def convert_to_mif(self) -> Path:
        """
        Creates a *.mif* version of this scan using mrconvert_.

        .. _mrconvert:
           https://mrtrix.readthedocs.io/en/latest/reference/commands/mrconvert.html

        Returns
        -------
        Path
            Created file path
        """
        from django_mri.analysis.utils.get_mrconvert_node import \
            get_mrconvert_node

        node, created = get_mrconvert_node()
        out_file = self.get_default_mif_path()
        if not out_file.parent.exists():
            out_file.parent.mkdir()
        return node.run(
            inputs={
                "in_file": self.nifti,
                "out_file": out_file,
                "in_bval": self.nifti.b_value_file,
                "in_bvec": self.nifti.b_vector_file,
            }
        )

    def get_default_mif_path(self) -> Path:
        """
        Returns the default *.mif* path for this scan.

        Returns
        -------
        Path
            Default *.mif* path
        """
        return get_mri_root() / "mif" / f"{self.id}.mif"

    def get_dicom_representation(self) -> str:
        """
        Returns the expected DICOM representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value DICOM representation of this scan

        See Also
        --------
        :property:`dicom_representation`
        """
        if self.dicom:
            return str(self.dicom.path)

    def get_nifti_representation(self) -> str:
        """
        Returns the expected NIfTI representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value NIfTI representation of this scan

        See Also
        --------
        :property:`nifti_representation`
        """
        if self._nifti:
            return str(self._nifti.path)

    def get_mif_representation(self) -> str:
        """
        Returns the expected *.mif* representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value NIfTI representation of this scan

        See Also
        --------
        :property:`mif_representation`
        """
        destination = self.get_default_mif_path()
        if destination.exists():
            return str(destination)

    def query_input_set(self) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.input.input.Input` subclass instances
        in which this scan is represented.

        Returns
        -------
        models.QuerySet
            Input queryset
        """
        all_input_ids = []
        for InputClass, filter_key in self.DERIVATIVE_QUERY.items():
            query = models.Q()
            for representation in self.REPRESENTATIONS:
                value = getattr(self, representation, None)
                if value is not None:
                    query |= models.Q(**{filter_key: value})
                inputs = InputClass.objects.filter(query)
                input_ids = list(inputs.values_list("id", flat=True))
                all_input_ids += input_ids
        return Input.objects.filter(id__in=all_input_ids).select_subclasses()

    def query_run_set(self) -> models.QuerySet:
        """
        Returns a queryset of :class:`~django_analyses.models.run.Run`
        instances in which this scan was included in the inputs.

        Returns
        -------
        models.QuerySet
            Input queryset
        """
        run_ids = self.input_set.values_list("run", flat=True)
        return Run.objects.filter(id__in=run_ids)

    def query_derivatives(self) -> Dict[Run, Dict[str, Any]]:
        """
        Returns a dictionary of associated runs and their outputs.

        Returns
        -------
        Dict[Run, Dict[str, Any]]
            Derivatives
        """
        return {run: run.output_configuration for run in self.query_run_set()}

    def html_plot(self):
        # First make sure an associated NIfTI instance exists or create it.
        if not self._nifti:
            try:
                self.dicom_to_nifti()
            except RuntimeError as e:
                # In case NIfTI conversion fails, return exception message.
                message = messages.NIFTI_CONVERSION_FAILURE_HTML.format(
                    scan_id=self.id, exception=e
                )
                return message
            else:
                if not isinstance(self._nifti, NIfTI):
                    e = "NIfTI format generation failure"
                    message = messages.NIFTI_CONVERSION_FAILURE_HTML.format(
                        scan_id=self.id, exception=e
                    )
                    return message
        # Determine the number of dimensions.
        has_3d_flag = any(
            [flag in self.description.lower() for flag in FLAG_3D]
        )
        has_4d_flag = any(
            [flag in self.description.lower() for flag in FLAG_4D]
        )
        if not (has_3d_flag or has_4d_flag):
            data = self.nifti.get_data()
            ndim = data.ndim
        else:
            ndim = 3 if has_3d_flag else 4
        # 3D parameters.
        if ndim == 3:
            image = str(self.nifti.path)
            title = self.description
        # 4D parameters.
        elif ndim == 4:
            image = mean_img(str(self.nifti.path))
            title = f"{self.description} (Mean Image)"
        return view_img(
            image,
            bg_img=False,
            cmap=cm.black_blue,
            symmetric_cmap=False,
            title=title,
        )

    def get_file_paths(self, file_format: Union[List[str], str] = None) -> List[Path]:
        if isinstance(file_format, str):
            file_format = [file_format]
        paths = []
        file_format = (
            ["dicom", "nifti"]
            if file_format is None
            else [f.lower() for f in file_format]
        )
        if hasattr(self, "dicom") and "dicom" in file_format:
            paths += self.dicom.get_file_paths()
        if self._nifti and "nifti" in file_format:
            paths += self.nifti.get_file_paths()
        return paths

    @property
    def bids_manager(self):
        """
        Returns the initialized instance of *BidsManger*
        Returns
        -------
        BidsManager
            A app-level BIDS data manager
        """
        if self._bids_manager is None:
            self._bids_manager = get_bids_manager()
        return self._bids_manager

    @property
    def mif(self) -> Path:
        """
        Returns the *.mif* version of this scan, creating it if it doesn't
        exist.

        Returns
        -------
        Path
            *.mif* file path

        See Also
        --------
        * :meth:`convert_to_mif`
        """

        destination = self.get_default_mif_path()
        if not destination.exists():
            self.convert_to_mif()
        return destination

    @property
    def mif_representation(self) -> str:
        """
        Returns the expected *.mif* representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value NIfTI representation of this scan

        See Also
        --------
        :func:`get_mif_representation`
        """
        return self.get_mif_representation()

    @property
    def sequence_type(self) -> str:
        """
        Returns the sequence type instance fitting this scan if one exists.

        See Also
        --------
        * :meth:`infer_sequence_type`

        Returns
        -------
        str
            Inferred sequence type
        """
        return self.infer_sequence_type()

    @property
    def nifti(self) -> NIfTI:
        """
        Returns the associated :class:`~django_mri.models.nifti.NIfTI` instance
        if one exists, or tries to create one if it doesn't.

        Returns
        -------
        NIfTI
            Associated NIfTI instance
        """
        if not isinstance(self._nifti, NIfTI):
            self.dicom_to_nifti()
        return self._nifti

    @property
    def nifti_representation(self) -> str:
        """
        Returns the expected NIfTI representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value NIfTI representation of this scan

        See Also
        --------
        :func:`get_nifti_representation`
        """
        return self.get_nifti_representation()

    @property
    def dicom_representation(self) -> str:
        """
        Returns the expected DICOM representation of this scan as part of any
        analysis' input specification.

        Returns
        -------
        str
            Input value DICOM representation of this scan

        See Also
        --------
        :func:`get_dicom_representation`
        """
        return self.get_dicom_representation()

    @property
    def subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the scan. If the
        subject's date of birth or the scan's acquisition time are not
        available, returns `None`.

        Returns
        -------
        float
            Subject age in years at the time of the scan's acquisition
        """
        conditions = (
            self.time
            and self.session
            and self.session.subject
            and self.session.subject.date_of_birth
        )
        if conditions:
            delta = self.time.date() - self.session.subject.date_of_birth
            return delta.total_seconds() / (60 * 60 * 24 * 365)

    @property
    def input_set(self) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.input.input.Input` subclass instances
        in which this scan is represented.

        Returns
        -------
        models.QuerySet
            Input queryset

        See Also
        --------
        :func:`query_input_set`
        """
        return self.query_input_set()

    # @property
    # def run_set(self) -> models.QuerySet:
    #     """
    #     Returns a queryset of :class:`~django_analyses.models.run.Run`
    #     instances in which this scan was included in the inputs.

    #     Returns
    #     -------
    #     models.QuerySet
    #         Input queryset

    #     See Also
    #     --------
    #     :func:`query_run_set`
    #     """
    #     return self.query_run_set()
