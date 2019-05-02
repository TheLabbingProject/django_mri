import django_dicom.data_import
import itertools
import os

from django_mri.models import NIfTI


class LocalImport:
    """
    Import new MRI data to the database. Currently only two file formats are
    supported; DICOM and NIfTI. The result of running this is the creation of new
    DICOM and NIfTI instances, but **NOT** of :class:`~django_mri.models.scan.Scan`
    instances. These are meant to be created after review by a researcher.
    
    """

    def __init__(self, path: str):
        """
        Initializes the :class:`~django_mri.data_import.local_import.LocalImport`
        class with the base directory path.
        
        Parameters
        ----------
        path : str
            Base directory for local MRI data import.
        """

        self.path = path

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

    def import_nifti_files(self, verbose: bool = True):
        """
        Imports NIfTI_ (*.nii* files) from the given directory tree.

        .. _NIfTI: https://nifti.nimh.nih.gov/
        
        Parameters
        ----------
        verbose : bool, optional
            Prints user friendly information during the run, by default True
        """

        if verbose:
            print("\nImporting NIfTI image files:")

        # NIfTI files are often compressed
        uncompressed_nii_files = self.path_generator(extension="nii")
        compressed_nii_files = self.path_generator(extension="nii.gz")
        nii_files = itertools.chain(uncompressed_nii_files, compressed_nii_files)

        # Create NIfTI instances in the database
        for nii in nii_files:
            if verbose:
                print(f"Importing {nii}...", end="\t")
            NIfTI.objects.create(path=nii, is_raw=True)
            if verbose:
                print("done!")

    def run(self, verbose: bool = True):
        """
        Import all supported MRI data files from the given directory tree.
        
        Parameters
        ----------
        verbose : bool, optional
            Prints user friendly information during the run, by default True
        """
        # Import DICOM data
        django_dicom.data_import.LocalImport(self.path).run(verbose=verbose)
        # Import NIfTI data
        self.import_nifti_files(verbose=verbose)

