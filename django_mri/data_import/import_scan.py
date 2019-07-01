from django.apps import apps
from django.conf import settings
from django_dicom.data_import.import_image import ImportImage
from django_mri.models.scan import Scan
from io import BufferedReader


subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)


class ImportScan:
    def __init__(
        self, subject: Subject, scan_file: BufferedReader, scan_type: str = "dcm"
    ):
        self.subject = subject
        self.scan_file = scan_file
        self.scan_type = scan_type

    def import_dicom_image(self):
        dicom_image, _ = ImportImage(self.scan_file).run()
        scan, created = Scan.objects.get_or_create(dicom=dicom_image.series)
        if created:
            scan.update_fields_from_dicom()
        scan.subject = self.subject
        scan.save()
        return scan, created

    def run(self) -> tuple:
        if self.scan_type == "dcm":
            return self.import_dicom_image()
        else:
            raise ValueError("Invalid scan type!")

