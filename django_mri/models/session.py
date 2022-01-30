"""
Definition of the :class:`Session` class.
"""
import logging
import shutil
from pathlib import Path
from typing import List

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_analyses.models.input.definitions.integer_input_definition import (
    IntegerInputDefinition,
)
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from django_analyses.models.input.types.integer_input import IntegerInput
from django_analyses.models.input.types.list_input import ListInput
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel
from django_mri.models import help_text, logs
from django_mri.models.managers.session import SessionQuerySet
from django_mri.utils import (
    get_bids_dir,
    get_group_model,
    get_measurement_model,
    get_study_model,
    get_subject_model,
)

Group = get_group_model()
MeasurementDefinition = get_measurement_model()
Study = get_study_model()
Subject = get_subject_model()

SECONDS_IN_YEAR: int = 60 * 60 * 24 * 365
CLAIMED_SESSION_STRING: str = "Subject #{subject_id} MRI session from {date}"
UNCLAIMED_SESSION_STRING: str = "Unclaimed MRI session from {date}"
DICOM_FILES_KEY: str = "dicom__image__dcm"
NIFTI_FILES_KEY: str = "_nifti__path"


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: The associated `Subject` model (optional).
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="mri_session_set",
        blank=True,
        null=True,
    )

    #: Any other information about this scanning sequence.
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=help_text.SESSION_COMMENTS,
    )

    #: The associated `Measurement` model (optional).
    measurement = models.ForeignKey(
        MeasurementDefinition,
        related_name="mri_session_set",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    #: The date and time in which this scanning sequence began.
    time = models.DateTimeField()

    #: Associated IRB approval.
    irb = models.ForeignKey(
        "django_mri.IrbApproval",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="IRB approval",
    )

    objects = SessionQuerySet.as_manager()

    BIDS_DIR_TEMPLATE: str = "ses-{date}{time}"
    SESSION_DATE_FORMAT: str = "%Y%m%d"
    SESSION_TIME_FORMAT: str = "%H%M"

    _logger = logging.getLogger("data.mri.session")

    class Meta:
        ordering = ("-time",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        date = self.time.date()
        if self.subject:
            return CLAIMED_SESSION_STRING.format(
                subject_id=self.subject.id, date=date
            )
        return UNCLAIMED_SESSION_STRING.format(date=date)

    def infer_subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the session
        acquisition. If the subject's date of birth or the session's
        acquisition time are not available, returns `None`.

        See Also
        --------
        * :func:`subject_age`

        Returns
        -------
        float
            Subject age in years at the time of the session's acquisition
        """
        has_required_info = (
            self.time and self.subject and self.subject.date_of_birth
        )
        if has_required_info:
            delta = self.time.date() - self.subject.date_of_birth
            return delta.total_seconds() / SECONDS_IN_YEAR

    def list_dicom_files(self) -> List[Path]:
        """
        Returns a list of the *.dcm* paths that make up the entire raw session
        data.

        Returns
        -------
        List[Path]
            *.dcm* files
        """
        return [
            Path(p)
            for p in self.scan_set.values_list(DICOM_FILES_KEY, flat=True)
        ]

    def list_nifti_files(self) -> List[Path]:
        """
        Returns a list of *.nii* files (and by default also JSON sidecars)
        included in this session.

        Returns
        -------
        List[Path]
            *.nii* files
        """
        paths = []
        for scan in self.scan_set.all(_nifti__isnull=False):
            nii_paths = scan.nifti.get_file_paths()
            paths += nii_paths
        return paths

    def query_measurement_studies(self) -> models.QuerySet:
        if self.measurement:
            return Study.objects.filter(
                id__in=self.measurement.procedure_set.values("study")
            )
        return Study.objects.none()

    def query_study_groups(self) -> models.QuerySet:
        return Group.objects.filter(
            id__in=self.scan_set.values("study_groups")
        ).distinct()

    def query_studies(self) -> models.QuerySet:
        return Study.objects.filter(
            id__in=self.study_groups.values("study__id")
        ).distinct()

    def query_run_set(self) -> models.QuerySet:
        content_type = ContentType.objects.get_for_model(self)
        list_input_definitions = ListInputDefinition.objects.filter(
            content_type=content_type
        )
        integer_input_definitions = IntegerInputDefinition.objects.filter(
            content_type=content_type
        )
        list_inputs = ListInput.objects.filter(
            definition__in=list_input_definitions, value__contains=self.id
        )
        integer_inputs = IntegerInput.objects.filter(
            definition__in=integer_input_definitions, value=self.id
        )
        run_ids = set(list_inputs.values_list("run", flat=True)) | set(
            integer_inputs.values_list("run", flat=True)
        )
        runs = Run.objects.none()
        for scan in self.scan_set.all():
            runs |= scan.query_run_set()
        return Run.objects.filter(id__in=run_ids) | runs

    def get_bids_dir(self) -> Path:
        bids_root = get_bids_dir()
        date = self.time.date().strftime(self.SESSION_DATE_FORMAT)
        time = self.time.time().strftime(self.SESSION_TIME_FORMAT)
        session_dir_name = self.BIDS_DIR_TEMPLATE.format(date=date, time=time)
        return bids_root / session_dir_name

    def delete_bids_dir(self):
        # Log BIDS directory deletion start.
        delete_start_log = logs.SESSION_BIDS_DELETE_START.format(pk=self.id)
        self._logger.debug(delete_start_log)
        path = self.get_bids_dir()
        if path.is_dir():
            # Delete.
            try:
                shutil.rmtree(path)
            except Exception as e:
                # Log exception and re-raise.
                failure_log = logs.SESSION_BIDS_DELETE_FAILURE.format(
                    pk=self.id, path=path, exception=e
                )
                self._logger.warn(failure_log)
                raise
            else:
                # Log existing directory deletion success.
                delete_end_log = logs.SESSION_BIDS_DELETE_END.format(
                    pk=self.id, path=path
                )
                self._logger.debug(delete_end_log)
        else:
            # Log no directory found at the expected path.
            abort_log = logs.SESSION_BIDS_DELETE_EMPTY.format(
                pk=self.id, path=path
            )
            self._logger.debug(abort_log)

    def convert_to_nifti(
        self,
        force: bool = False,
        persistent: bool = True,
        progressbar: bool = False,
        progressbar_position: int = 0,
    ):
        # Log session data conversion start.
        start_log = logs.SESSION_NIFTI_CONVERSION_START.format(pk=self.id)
        self._logger.debug(start_log)
        # If *force* is True, start off by deleting the existing BIDS
        # directory for this session, which should contain prior (supported)
        # conversion results.
        if force:
            self.delete_bids_dir()
        try:
            self.scan_set.convert_to_nifti(
                force=force,
                persistent=persistent,
                progressbar=progressbar,
                progressbar_position=progressbar_position,
            )
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SESSION_NIFTI_CONVERSION_FAILURE.format(
                pk=self.id, exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log session data conversion success.
            success_log = logs.SESSION_NIFTI_CONVERSION_END.format(pk=self.id)
            self._logger.debug(success_log)

    @property
    def subject_age(self) -> float:
        """
        Returns the subject's age in years at the time of the session
        acquisition. If the subject's date of birth or the session's
        acquisition time are not available, returns `None`.

        See Also
        --------
        * :func:`infer_subject_age`

        Returns
        -------
        float
            Subject age in years at the time of the session's acquisition
        """
        return self.infer_subject_age()

    @property
    def study_groups(self) -> models.QuerySet:
        """
        Returns a queryset of associated :class:`~research.models.group.Group`
        instances.

        Returns
        -------
        models.QuerySet
            Associated study groups
        """
        return self.query_study_groups()
