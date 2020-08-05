from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager
from django_dicom.models.image import Image as DicomImage
from django_mri.utils.scan_type import ScanType
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

    def create(self, **obj_data):
        try:
            scan = self.get(dicom=obj_data["dicom"])
            return scan
        except ObjectDoesNotExist:
            return super().create(**obj_data)
