# from django.apps import apps
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.db.models import ObjectDoesNotExist
# from django_dicom.models.image import Image
# from django_mri.data_import.utils.create_progressbar import create_progressbar
# from django_mri.models.scan import Scan
# from django_mri.utils.scan_type import ScanType
# from pathlib import Path


# subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
# Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)
# User = get_user_model()


# class ImportScan:
#     def __init__(
#         self,
#         subject: Subject,
#         path: Path,
#         scan_type: ScanType = ScanType.DICOM,
#         user: User = None,
#     ):
#         self.subject = subject
#         self.path = Path(path)
#         self.scan_type = scan_type
#         self.user = user

#     def import_dicom_image(self, path: Path) -> tuple:
#         image, created = Image.objects.import_path(path)
#         try:
#             scan = Scan.objects.get(dicom=image.series)
#             return scan, False
#         except ObjectDoesNotExist:
#             scan = Scan.objects.create(
#                 dicom=image.series, subject=self.subject, added_by=self.user
#             )
#             return scan, True

#     def import_dicom_data(self) -> tuple:
#         scans = []
#         any_created = False
#         progressbar = create_progressbar(self.path.rglob("*.dcm"), unit="image")
#         for path in progressbar:
#             scan, created = self.import_dicom_image(path)
#             any_created = any_created or created
#             if scan not in scans:
#                 scans.append(scan)
#         return scans, any_created

#     def run(self) -> tuple:
#         if self.scan_type == ScanType.DICOM:
#             return Image.objects.import_path(self.path)
#         else:
#             raise ValueError("Invalid scan type!")
