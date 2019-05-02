import numpy as np

from django.test import TestCase
from django_dicom.data_import import LocalImport
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from tests.fixtures import (
    DICOM_SERIES_PATH,
    SIEMENS_DWI_SERIES,
    SIEMENS_DWI_SERIES_PATH,
)


class NIfTIModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        LocalImport(DICOM_SERIES_PATH).run(verbose=False)
        LocalImport(SIEMENS_DWI_SERIES_PATH).run(verbose=False)

    def setUp(self):
        self.simple_scan = Scan.objects.first()
        self.dwi_scan = Scan.objects.last()
        if not self.simple_scan or not self.dwi_scan:
            self.fail("Test scan not created! Check signals.")
        self.simple_nifti = self.simple_scan.nifti
        self.dwi_nifti = self.dwi_scan.nifti

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
        destination = self.dwi_scan.get_default_nifti_destination()
        expected = destination + ".nii.gz"
        self.assertEqual(self.dwi_nifti.path, expected)

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
        data = self.dwi_nifti.get_data()
        self.assertIsInstance(data, np.ndarray)

    def test_get_b_value(self):
        result = self.dwi_nifti.get_b_value()
        self.assertListEqual(result, SIEMENS_DWI_SERIES["b_value"])

    def test_get_b_vector(self):
        result = self.dwi_nifti.get_b_vector()
        self.assertListEqual(result, SIEMENS_DWI_SERIES["b_vector"])

    ##############
    # Properties #
    ##############

    def test_b_value(self):
        result = self.dwi_nifti.b_value
        expected = self.dwi_nifti.get_b_value()
        self.assertListEqual(result, expected)

    def test_b_value_for_non_DWI_returns_none(self):
        self.assertIsNone(self.simple_nifti.b_value)

    def test_b_vector(self):
        result = self.dwi_nifti.b_vector
        expected = self.dwi_nifti.get_b_vector()
        self.assertListEqual(result, expected)

    def test_b_vector_for_non_DWI_returns_none(self):
        self.assertIsNone(self.simple_nifti.b_vector)

    def test_subject_id(self):
        subject_id = "TESTSUB"
        self.simple_scan.subject_id = subject_id
        self.assertEqual(self.simple_nifti.subject_id, subject_id)

    def test_subject_id_with_no_subject(self):
        self.assertIsNone(self.dwi_nifti.subject_id)
