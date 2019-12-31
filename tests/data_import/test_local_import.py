import os

from django.test import TestCase
from django_dicom.models import Series, Image
from django_mri.data_import.local_import import LocalImport
from django.contrib.auth import get_user_model
# from django_mri.models import NIfTI
from tests.fixtures import TEST_FILES_PATH, LONELY_FILES_PATH
from ..models import Subject  # , Group


class LocalImportTestCase(TestCase):
    def setUp(self):
        LONELY_FILES_DCM_1 = os.path.join(LONELY_FILES_PATH, '001.dcm')
        LONELY_FILES_ZIP_1 = os.path.join(LONELY_FILES_PATH, '001.zip')
        User = get_user_model()
        self.user = User.objects.create()
        self.subject = Subject.objects.create()
        self.importer = LocalImport(self.subject, TEST_FILES_PATH, self.user)
        self.importer_dcm = LocalImport(self.subject, LONELY_FILES_DCM_1, self.user)
        self.importer_zip = LocalImport(self.subject, LONELY_FILES_ZIP_1, self.user)

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
        for path in LocalImport(self.subject, TEST_FILES_PATH).path_generator():
            is_valid_path = os.path.isfile(path)
            self.assertTrue(is_valid_path)
            is_under_base_dir = path.startswith(TEST_FILES_PATH)
            self.assertTrue(is_under_base_dir)
            counter += 1
        self.assertEqual(counter, 42)

    def test_path_generator_with_extension(self):
        """
        Tests the :meth:`~django_mri.data_import.local_import.LocalImport.path_generator`
        method with the *extension* parameter set.
        
        """

        # A dictionary of extensions and the number of files we expect
        extensions = {"nii.gz": 1, "dcm": 40}

        for extension in extensions:
            counter = 0
            generator = LocalImport(self.subject, TEST_FILES_PATH).path_generator(extension=extension)
            for path in generator:
                is_valid_path = os.path.isfile(path)
                self.assertTrue(is_valid_path)
                is_under_base_dir = path.startswith(TEST_FILES_PATH)
                self.assertTrue(is_under_base_dir)
                counter += 1
            self.assertEqual(counter, extensions.get(extension))

    # def test_import_nifti_files(self):
    #     self.importer.import_nifti_files(verbose=False)
    #     self.assertEqual(NIfTI.objects.count(), 1)
    #     NIfTI.objects.all().delete()

    def test_run(self):
        self.importer.run()
        # self.assertEqual(NIfTI.objects.count(), 1)
        self.assertEqual(Series.objects.count(), 4)

    def test_run_one_dcm(self):
        self.importer_dcm.run()
        self.assertEqual(Image.objects.count(), 1)

    def test_run_one_zip(self):
        self.importer_zip.run()
        self.assertEqual(Image.objects.count(), 3)
