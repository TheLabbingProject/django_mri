from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager
from django_dicom.models.image import Image as DicomImage
from django_mri.utils.scan_type import ScanType
from django_mri.models.sequence_type import SequenceType
from pathlib import Path


class ScanManager(Manager):
    def import_dicom_data(
        self, path: Path, progressbar: bool = True, report: bool = True
    ) -> tuple:
        images = DicomImage.objects.import_path(
            path, progressbar=progressbar, report=report
        )
        series = set([image.series for image in images])
        scans = self.filter(dicom__in=series)
        return scans

    def import_path(
        self, path: Path, progressbar: bool = True, report: bool = True
    ) -> tuple:
        dicom_scans = self.import_dicom_data(path, progressbar, report)
        return {ScanType.DICOM.value: dicom_scans}

    def scan_by_method(self, method: str) -> list:
        mri_method_definitions = SequenceType.objects.get(
            title__iexact=method
        ).sequence_definitions
        sequence_variants = map(
            lambda definition: definition["sequence_variant"],
            mri_method_definitions,
        )
        scanning_sequences = map(
            lambda definition: definition["scanning_sequence"],
            mri_method_definitions,
        )
        return self.filter(
            dicom__sequence_variant__contains=list(sequence_variants),
            dicom__scanning_sequence__contains=list(scanning_sequences),
        )
