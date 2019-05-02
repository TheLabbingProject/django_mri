import os

from django.test import TestCase
from django_dicom.models import Series
from django_mri.data_import.local_import import LocalImport
from django_mri.models import NIfTI
from tests.fixtures import TEST_FILES_PATH


class LocalImportTestCase(TestCase):
    def setUp(self):
        self.importer = LocalImport(TEST_FILES_PATH)

    def test_initialization(self):
        result = self.importer.path
        expected = TEST_FILES_PATH
        self.assertEqual(result, expected)

    def test_path_generator_without_extension(self):
        """
        Tests the :meth:`~django_mri.data_import.local_import.LocalImport.path_generator`
        method with no *extension* parameter setting.
        
        """

        counter = 0
        for path in LocalImport(TEST_FILES_PATH).path_generator():
            is_valid_path = os.path.isfile(path)
            self.assertTrue(is_valid_path)
            is_under_base_dir = path.startswith(TEST_FILES_PATH)
            self.assertTrue(is_under_base_dir)
            counter += 1
        self.assertEqual(counter, 40)

    def test_path_generator_with_extension(self):
        """
        Tests the :meth:`~django_mri.data_import.local_import.LocalImport.path_generator`
        method with the *extension* parameter set.
        
        """

        # A dictionary of extensions and the number of files we expect
        extensions = {"nii.gz": 1, "dcm": 39}

        for extension in extensions:
            counter = 0
            generator = LocalImport(TEST_FILES_PATH).path_generator(extension=extension)
            for path in generator:
                is_valid_path = os.path.isfile(path)
                self.assertTrue(is_valid_path)
                is_under_base_dir = path.startswith(TEST_FILES_PATH)
                self.assertTrue(is_under_base_dir)
                counter += 1
            self.assertEqual(counter, extensions.get(extension))

    def test_import_nifti_files(self):
        self.importer.import_nifti_files(verbose=False)
        self.assertEqual(NIfTI.objects.count(), 1)
        NIfTI.objects.all().delete()

    def test_run(self):
        self.importer.run(verbose=False)
        self.assertEqual(NIfTI.objects.count(), 1)
        self.assertEqual(Series.objects.count(), 2)
