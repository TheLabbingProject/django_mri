import os
import zipfile

from django.apps import apps
from django.contrib.auth import get_user_model
from django.conf import settings
from django_mri.data_import.import_scan import ImportScan


subject_app_label, subject_model_name = settings.SUBJECT_MODEL.split(".")
Subject = apps.get_model(app_label=subject_app_label, model_name=subject_model_name)
User = get_user_model()


class LocalImport:
    """
    Import new MRI data to the database. Currently only two file formats are
    supported; DICOM and NIfTI. The result of running this is the creation of new
    DICOM and NIfTI instances, but **NOT** of :class:`~django_mri.models.scan.Scan`
    instances. These are meant to be created after review by a researcher.
    
    """

    def __init__(self, subject: Subject, path: str, user: User = None):
        """
        Initializes the :class:`~django_mri.data_import.local_import.LocalImport`
        class with the base directory path.
        
        Parameters
        ----------
        subject : Subject
            The research subject to whom the scan belongs.
        path : str
            Base directory for local MRI data import.
        """

        self.subject = subject
        self.path = path
        self.user = user

    @classmethod
    def import_local_dcm(cls, subject: Subject, path: str, user: User = None) -> tuple:
        """
        Imports a single DICOM image (.dcm file) using *django_dicom*'s
        :class:`~django_dicom.data_import.import_scan.ImportScan` class.
        
        Parameters
        ----------
        subject : Subject
            The research subject to whom the scan belongs.
        path : str
            Full path of the DICOM image.
        
        Returns
        -------
        tuple
            (Resulting :class:`~django_dicom.models.image.Image` instance, Created [bool])
        """

        with open(path, "rb") as dcm_buffer:
            return ImportScan(subject, dcm_buffer, scan_type="dcm", user=user).run()

    def import_zip_archive(cls, subject: Subject, path: str, user: User = None) -> None:
        """
        Iterates over the files within a ZIP archive and imports any "*.dcm*" files.
        
        Parameters
        ----------
        path : str
            Local ZIP archive path.
        verbose : bool, optional
            Show a progressbar (default to True).
        """

        with zipfile.ZipFile(path, "r") as archive:
            for file_name in archive.namelist():
                if file_name.endswith(".dcm"):
                    with archive.open(file_name) as dcm_buffer:
                        ImportScan(
                            subject, dcm_buffer, scan_type="dcm", user=user
                        ).run()

    def path_generator(self, extension: str = "") -> str:
        """
        Generates paths from the given directory tree.

        Parameters
        ----------
        extension : str
            A file extension to filter the generated files with.
        
        Returns
        -------
        str
            File path.
        """

        for directory, _, files in os.walk(self.path):
            if extension:
                files = [f for f in files if f.endswith(f".{extension}")]
            for file_name in files:
                yield os.path.join(directory, file_name)

    # def import_nifti_files(self, verbose: bool = True):
    #     """
    #     Imports NIfTI_ (*.nii* files) from the given directory tree.

    #     .. _NIfTI: https://nifti.nimh.nih.gov/

    #     Parameters
    #     ----------
    #     verbose : bool, optional
    #         Prints user friendly information during the run, by default True
    #     """

    #     if verbose:
    #         print("\nImporting NIfTI image files:")

    #     # NIfTI files are often compressed
    #     uncompressed_nii_files = self.path_generator(extension="nii")
    #     compressed_nii_files = self.path_generator(extension="nii.gz")
    #     nii_files = itertools.chain(uncompressed_nii_files, compressed_nii_files)

    #     # Create NIfTI instances in the database
    #     for nii in nii_files:
    #         if verbose:
    #             print(f"Importing {nii}...", end="\t")
    #         NIfTI.objects.create(path=nii, is_raw=True)
    #         if verbose:
    #             print("done!")

    def run(self):
        """
        Import all supported MRI data files from the given directory tree.
        
        """

        if os.path.isdir(self.path):
            dcm_generator = self.path_generator(extension="dcm")
            for dcm_path in dcm_generator:
                self.import_local_dcm(self.subject, dcm_path, user=self.user)
            archives = self.path_generator(extension="zip")
            for archive in archives:
                self.import_zip_archive(self.subject, archive, user=self.user)

        elif os.path.isfile(self.path):
            if self.path.endswith(".dcm"):
                self.import_local_dcm(self.subject, self.path, user=self.user)
            elif self.path.endswith(".zip"):
                self.import_zip_archive(self.subject, self.path, user=self.user)
