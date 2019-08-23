from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django_dicom.data_import.import_image import ImportImage
from django_mri.models.scan import Scan
from io import BufferedReader


subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)
User = get_user_model()


class ImportScan:
    def __init__(
        self,
        subject: Subject,
        scan_file: BufferedReader,
        scan_type: str = "dcm",
        user: User = None,
    ):
        self.subject = subject
        self.scan_file = scan_file
        self.scan_type = scan_type
        self.user = user

    def import_dicom_image(self):
        dicom_image, _ = ImportImage(self.scan_file).run()
        scan, created = Scan.objects.get_or_create(dicom=dicom_image.series)
        if created:
            scan.update_fields_from_dicom()
            if self.user:
                scan.added_by = self.user
        scan.subject = self.subject
        scan.save()
        return scan, created

    def run(self) -> tuple:
        if self.scan_type == "dcm":
            return self.import_dicom_image()
        else:
            raise ValueError("Invalid scan type!")

