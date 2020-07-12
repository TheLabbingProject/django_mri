# import os
# import zipfile

# from django.apps import apps
# from django.contrib.auth import get_user_model
# from django.conf import settings
# from django_dicom.data_import.local_import import LocalImport as LocalDicomImport
# from django_mri.data_import.import_scan import ImportScan
# from django_mri.data_import.utils.create_progressbar import create_progressbar
# from django_mri.data_import.utils.path_generator import path_generator
# from pathlib import Path


# subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
# Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)
# User = get_user_model()


# class LocalImport:
#     """
#     Import new MRI data to the database. Currently only two file formats are
#     supported; DICOM and NIfTI. The result of running this is the creation of new
#     DICOM and NIfTI instances, but **NOT** of :class:`~django_mri.models.scan.Scan`
#     instances. These are meant to be created after review by a researcher.

#     """

#     def __init__(self, subject: Subject, path: str, user: User = None):
#         """
#         Initializes the :class:`~django_mri.data_import.local_import.LocalImport`
#         class with the base directory path.

#         Parameters
#         ----------
#         subject : Subject
#             The research subject to whom the scan belongs.
#         path : str
#             Base directory for local MRI data import.
#         """

#         self.subject = subject
#         self.path = path
#         self.user = user

#     def import_zip_archive(cls, subject: Subject, path: str, user: User = None) -> None:
#         """
#         Iterates over the files within a ZIP archive and imports any "*.dcm*" files.

#         Parameters
#         ----------
#         path : str
#             Local ZIP archive path.
#         verbose : bool, optional
#             Show a progressbar (default to True).
#         """

#         with zipfile.ZipFile(path, "r") as archive:
#             for file_name in archive.namelist():
#                 if file_name.endswith(".dcm"):
#                     with archive.open(file_name) as dcm_buffer:
#                         ImportScan(
#                             subject, dcm_buffer, scan_type="dcm", user=user
#                         ).run()

#     def run(self):
#         """
#         Import all supported MRI data files from the given directory tree.

#         """

#         if os.path.isdir(self.path):
#             images, created = LocalDicomImport.from_path(self.path)

#         elif os.path.isfile(self.path):
#             if self.path.endswith(".dcm"):
#                 self.import_local_dcm(self.subject, self.path, user=self.user)
#             elif self.path.endswith(".zip"):
#                 self.import_zip_archive(self.subject, self.path, user=self.user)

#     @classmethod
#     def from_path(self, path: Path) -> tuple:
#         images, created = LocalDicomImport.from_path(path)
