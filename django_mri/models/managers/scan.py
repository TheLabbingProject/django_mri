"""
Definition of the :class:`ScanQuerySet` class.
"""
from itertools import chain
from pathlib import Path
from typing import Iterable, Union

from django.db.models import QuerySet
from django_dicom.models.image import Image as DicomImage
from tqdm import tqdm

from django_mri.utils.scan_type import ScanType


class ScanQuerySet(QuerySet):
    """
    Custom manager for the :class:`~django_mri.models.scan.Scan` class.
    """

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

    def sync_bids(self, progressbar: bool = True):
        iterator = tqdm(self.all()) if progressbar else self.all()
        for scan in iterator:
            scan.sync_bids()
