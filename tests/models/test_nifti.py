import numpy as np

from django.test import TestCase
from django_dicom.data_import import LocalImport
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from tests.fixtures import DICOM_IMAGE_PATH


class NIfTIModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        LocalImport.import_local_dcm(DICOM_IMAGE_PATH)

    def setUp(self):
        self.scan = Scan.objects.first()
        if not self.scan:
            self.fail("Test scan not created! Check signals.")
        self.nifti = self.scan.nifti

    ##########
    # Fields #
    ##########

    # path
    def test_path_blank_and_null(self):
        field = NIfTI._meta.get_field("path")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_path_max_length(self):
        field = NIfTI._meta.get_field("path")
        self.assertEqual(field.max_length, 500)

    def test_path_value(self):
        destination = self.scan.get_default_nifti_destination()
        expected = destination + ".nii.gz"
        self.assertEqual(self.nifti.path, expected)

    # is_raw
    def test_is_raw_blank_and_null(self):
        field = NIfTI._meta.get_field("is_raw")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_is_raw_default(self):
        field = NIfTI._meta.get_field("is_raw")
        self.assertFalse(field.default)

    # parent
    def test_parent_blank_and_null(self):
        field = NIfTI._meta.get_field("parent")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_get_data(self):
        data = self.nifti.get_data()
        self.assertIsInstance(data, np.ndarray)

    # TODO: Fix test, doesn't work with single image given as dir
    # def test_get_b_value(self):
    #     result = self.nifti.get_b_value()
    #     expected = [0, 0, 100]
    #     self.assertListEqual(result, expected)

