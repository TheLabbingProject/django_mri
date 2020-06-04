# import os
# import factory
# import numpy as np

# from django.test import TestCase
# from django_mri.models.nifti import NIfTI
# from django_mri.models.scan import Scan
# from django_dicom.models import Image
# from tests.fixtures import (
#     DICOM_SERIES_PATH,
#     SIEMENS_DWI_SERIES,
#     SIEMENS_DWI_SERIES_PATH,
#     # IMPORTED_DICOM_FILES_PATH,
#     # IMPORTED_DICOM_DWI_PATH,
# )
# from tests.models import Subject

# # from tests.utils import restore_path
# from django.db.models import signals
# from pathlib import Path


# class NIfTIModelTestCase(TestCase):
#     @classmethod
#     @factory.django.mute_signals(signals.post_save)
#     def setUpTestData(cls):
#         cls.subject = Subject.objects.create()
#         Image.objects.import_path(Path(DICOM_SERIES_PATH))
#         Scan.objects.get_or_create(dicom=Image.objects.first().series)
#         Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
#         Scan.objects.get_or_create(dicom=Image.objects.last().series)

#     def setUp(self):
#         self.simple_scan = Scan.objects.first()
#         self.dwi_scan = Scan.objects.last()
#         if not self.simple_scan or not self.dwi_scan:
#             self.fail("Test scan not created! Check signals.")
#         self.simple_nifti = self.simple_scan.dicom_to_nifti()
#         self.dwi_nifti = self.dwi_scan.dicom_to_nifti()

#     # @classmethod
#     # def tearDownClass(cls):
#     #     scan = Scan.objects.last()
#     #     dwi_scan = Scan.objects.first()
#     #     curr_path = os.path.join(
#     #         IMPORTED_DICOM_FILES_PATH, scan.dicom.patient.uid, scan.dicom.uid
#     #     )
#     #     dwi_curr_path = os.path.join(
#     #         IMPORTED_DICOM_DWI_PATH, dwi_scan.dicom.patient.uid, dwi_scan.dicom.uid
#     #     )
#     #     restore_path(curr_path, DICOM_SERIES_PATH)
#     #     restore_path(dwi_curr_path, SIEMENS_DWI_SERIES_PATH)
#     #     super().tearDownClass()

#     ##########
#     # Fields #
#     ##########

#     # path
#     def test_path_blank_and_null(self):
#         field = NIfTI._meta.get_field("path")
#         self.assertFalse(field.blank)
#         self.assertFalse(field.null)

#     def test_path_max_length(self):
#         field = NIfTI._meta.get_field("path")
#         self.assertEqual(field.max_length, 1000)

#     def test_path_value(self):
#         destination = self.dwi_scan.get_default_nifti_destination()
#         expected = str(destination) + ".nii.gz"
#         result = str(self.dwi_nifti.path)
#         self.assertEqual(result, expected)

#     # is_raw
#     def test_is_raw_blank_and_null(self):
#         field = NIfTI._meta.get_field("is_raw")
#         self.assertFalse(field.blank)
#         self.assertFalse(field.null)

#     def test_is_raw_default(self):
#         field = NIfTI._meta.get_field("is_raw")
#         self.assertFalse(field.default)

#     ###########
#     # Methods #
#     ###########

#     def test_get_data(self):
#         data = self.dwi_nifti.get_data()
#         self.assertIsInstance(data, np.ndarray)

#     def test_get_b_value(self):
#         result = self.dwi_nifti.get_b_value()
#         self.assertListEqual(result, SIEMENS_DWI_SERIES["b_value"])

#     def test_get_b_vector(self):
#         result = self.dwi_nifti.get_b_vector()
#         self.assertListEqual(result, SIEMENS_DWI_SERIES["b_vector"])

#     ##############
#     # Properties #
#     ##############

#     def test_b_value(self):
#         result = self.dwi_nifti.b_value
#         expected = self.dwi_nifti.get_b_value()
#         self.assertEqual(result, expected)

#     def test_b_value_for_non_DWI_returns_none(self):
#         self.assertIsNone(self.simple_nifti.b_value)

#     def test_b_vector(self):
#         result = self.dwi_nifti.b_vector
#         expected = self.dwi_nifti.get_b_vector()
#         self.assertListEqual(result, expected)

#     def test_b_vector_for_non_DWI_returns_none(self):
#         self.assertIsNone(self.simple_nifti.b_vector)
