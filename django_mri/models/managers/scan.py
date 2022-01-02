"""
Definition of the :class:`ScanQuerySet` class.
"""
import logging
import warnings
from itertools import chain
from pathlib import Path
from typing import Iterable, List, Union

from django.db.models import Model, Q, QuerySet
from django_dicom.models.image import Image as DicomImage
from django_mri.models.managers import logs
from django_mri.utils.scan_type import ScanType
from tqdm import tqdm


class ScanQuerySet(QuerySet):
    """
    Custom manager for the :class:`~django_mri.models.scan.Scan` class.
    """

    _logger = logging.getLogger("data.mri.scan")

    def import_dicom_data(
        self, path: Path, progressbar: bool = True, report: bool = True
    ) -> QuerySet:
        """
        Imports DICOM files to the database using django_dicom_.

        .. _django_dicom:
           https://github.com/TheLabbingProject/django_dicom

        Parameters
        ----------
        path : Path
            Path to import *.dcm* files from
        progressbar : bool, optional
            Whether to print a progressbar or not, by default True
        report : bool, optional
            Whether to print a summary report, by default True

        Returns
        -------
        QuerySet
            The created DICOM
            :class:`~django_dicom.models.series.Series` instances
        """

        images = DicomImage.objects.import_path(
            path, progressbar=progressbar, report=report
        )
        series = set([image.series for image in images])
        scans = self.filter(dicom__in=series)
        return scans

    def import_path(
        self,
        path: Union[Path, Iterable[Path]],
        progressbar: bool = True,
        report: bool = True,
    ) -> dict:
        """
        Import MRI data from the given path.

        Parameters
        ----------
        path : Union[Path, Iterable[Path]]
            Path or paths to import *.dcm* files from
        progressbar : bool, optional
            Whether to print a progressbar or not, by default True
        report : bool, optional
            Whether to print a summary report, by default True

        Returns
        -------
        dict
            Created database instances by MRI scan type
        """

        if isinstance(path, (Path, str)):
            dicom_scans = self.import_dicom_data(path, progressbar, report)
        else:
            dicom_scans = list(
                chain(
                    *[
                        self.import_dicom_data(p, progressbar, report)
                        for p in path
                    ]
                )
            )
        return {ScanType.DICOM.value: dicom_scans}

    def delete_nifti(
        self, progressbar: bool = False, progressbar_position: int = 0,
    ):
        # Log NIfTI delete start.
        start_log = logs.SCAN_SET_NIFTI_DELETE_START.format(count=self.count())
        self._logger.debug(start_log)
        # Filter to only iterate scans with associated NIfTI instances.
        queryset = self.filter(_nifti__isnull=False)
        # Handle empty queryset.
        if not queryset.exists():
            # Log and return.
            abort_log = logs.SCAN_SET_NIFTI_DELETE_EMPTY.format(
                count=self.count()
            )
            self._logger.debug(abort_log)
            return
        iterator = (
            tqdm(
                queryset,
                unit="NIfTI",
                desc="Deleting",
                position=progressbar_position,
                leave=not progressbar_position,
            )
            if progressbar
            else queryset
        )
        # Delete associated NIfTI instances. This must be done by iteration
        # rather than an update, in order to trigger the post_save() signal
        # which removed the files from the media directory.
        n_deleted = 0
        try:
            for scan in iterator:
                scan.nifti.delete()
                n_deleted += 1
        except Exception as e:
            # Log exception and re-raise.
            failure_log = logs.SCAN_SET_NIFTI_DELETE_FAILURE.format(
                n_deleted=n_deleted, n_total=queryset.count(), exception=e
            )
            self._logger.warn(failure_log)
            raise
        else:
            # Log success and return.
            success_log = logs.SCAN_SET_NIFTI_DELETE_SUCCESS.format(
                count=self.count()
            )
            self._logger.debug(success_log)

    def sync_bids(
        self, progressbar: bool = True, log_level: int = logging.DEBUG
    ):
        queryset = self.order_by("number")
        iterator = tqdm(queryset) if progressbar else queryset
        for scan in iterator:
            scan.sync_bids(log_level=log_level)

    def convert_to_nifti(
        self,
        force: bool = False,
        persistent: bool = True,
        progressbar: bool = False,
        progressbar_position: int = 0,
    ):
        # Log start.
        start_log = logs.SCAN_SET_NIFTI_CONVERSION_START.format(
            count=self.count()
        )
        self._logger.debug(start_log)
        if force:
            self.delete_nifti(
                progressbar=progressbar,
                progressbar_position=progressbar_position,
            )
        # Run by scan order and create progressbar if required.
        queryset = self.filter(_nifti__isnull=True).order_by("number")
        # Query fieldmaps to convert only after their "IntendedFor" targets
        # have been converted (required for correct BIDS postprocessing).
        fieldmaps = queryset.filter(dicom__sequence_type__contains="fieldmap")
        non_fieldmaps = queryset.exclude(
            dicom__sequence_type__contains="fieldmap"
        )
        if fieldmaps.exists():
            # Log fieldmaps detected and will be converted in the end.
            fieldmaps_log = logs.SCAN_SET_NIFTI_CONVERSION_FIELDMAPS.format(
                n_fieldmaps=fieldmaps.count(), n_total=non_fieldmaps.count()
            )
            self._logger.debug(fieldmaps_log)
        non_fieldmaps_iterator = (
            tqdm(
                non_fieldmaps,
                unit="scan",
                desc="Scans",
                position=progressbar_position,
                leave=not progressbar_position,
            )
            if progressbar
            else non_fieldmaps
        )
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            # Convert non-fieldmap scans.
            for scan in non_fieldmaps_iterator:
                scan.dicom_to_nifti(persistent=persistent)
            # Convert fieldmaps.
            if fieldmaps.exists():
                fieldmap_iterator = (
                    tqdm(
                        fieldmaps,
                        unit="scan",
                        desc="Fieldmaps",
                        position=progressbar_position,
                        leave=not progressbar_position,
                    )
                    if progressbar
                    else fieldmaps
                )
                for fieldmap in fieldmap_iterator:
                    fieldmap.dicom_to_nifti(persistent=persistent)
        # Log conversion succcess.
        success_log = logs.SCAN_SET_NIFTI_CONVERSION_SUCCESS.format(
            count=queryset.count()
        )
        self._logger.debug(success_log)

    def filter_by_collaborators(
        self, collaborators: Union[Model, List[Model]]
    ) -> QuerySet:
        return self.filter(
            study_groups__study__collaborators=collaborators
        ).distinct()
