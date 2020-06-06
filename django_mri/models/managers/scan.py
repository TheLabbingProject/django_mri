from django.db.models import Manager
from django_dicom.models.image import Image as DicomImage
from django_mri.utils.scan_type import ScanType
from pathlib import Path


class ScanManager(Manager):
    def import_dicom_data(self, path: Path) -> tuple:
        images = DicomImage.objects.import_path(path)
        series = set([image.series for image in images])
        scans = self.filter(dicom__in=series)
        return scans

    def import_path(self, path: Path) -> tuple:
        dicom_scans = self.import_dicom_data(path)
        return {ScanType.DICOM.value: dicom_scans}
