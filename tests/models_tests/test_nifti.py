import factory
import numpy as np

from django.db.models import signals
from django.test import TestCase
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_dicom.models import Image
from tests.factories import SubjectFactory
from tests.fixtures import (
    DICOM_MPRAGE_PATH,
    SIEMENS_DWI_SERIES,
    SIEMENS_DWI_SERIES_PATH,
)
from pathlib import Path


class NIfTIModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        cls.subject = SubjectFactory()
        Image.objects.import_path(Path(DICOM_MPRAGE_PATH))
        series = Image.objects.first().series
        Scan.objects.get_or_create(dicom=series, subject=cls.subject)
        Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
        series_dwi = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_dwi, subject=cls.subject)

    def setUp(self):
        self.simple_scan = Scan.objects.first()
        self.dwi_scan = Scan.objects.last()
        if not self.simple_scan or not self.dwi_scan:
            self.fail("Test scan not created! Check signals.")
        try:
            self.simple_nifti = self.simple_scan.nifti
        except RuntimeError:
            destination = self.simple_scan.get_default_nifti_destination()
            # destination = self.simple_scan.get_bids_destination()
            expected = destination.with_suffix(
                ".nii"
            )  # In case the generated file is not compressed after several compression tests.
            if expected.is_file():
                self.simple_nifti = NIfTI.objects.create(
                    path=expected, is_raw=True
                )
            else:
                self.simple_nifti = self.simple_scan.nifti
        self.dwi_nifti = self.dwi_scan.dicom_to_nifti()

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
        self.assertEqual(field.max_length, 1000)

    def test_path_value(self):
        destination = self.dwi_scan.get_default_nifti_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.dwi_nifti.path)
        self.assertEqual(result, expected)

    # is_raw
    def test_is_raw_blank_and_null(self):
        field = NIfTI._meta.get_field("is_raw")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_is_raw_default(self):
        field = NIfTI._meta.get_field("is_raw")
        self.assertFalse(field.default)

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

    def test_uncompress_keep_source(self):
        source = Path(self.simple_nifti.path)
        expected = str(self.simple_nifti.path).replace(".gz", "")
        expected = Path(expected)
        result = self.simple_nifti.uncompress(keep_source=True)
        source.unlink()
        self.assertEqual(result, expected)

    def test_compress_keep_source(self):
        if self.simple_nifti.is_compressed:
            self.simple_nifti.uncompress()
        source = Path(self.simple_nifti.path)
        expected = str(self.simple_nifti.path) + ".gz"
        expected = Path(expected)
        result = self.simple_nifti.compress(keep_source=True)
        source.unlink()
        self.assertEqual(result, expected)

    def test_compress_already_compressed(self):
        if not self.simple_nifti.is_compressed:
            self.simple_nifti.compress()
        expected = str(self.simple_nifti.path)
        expected = Path(expected)
        result = self.simple_nifti.compress()
        self.assertEqual(result, expected)

    def test_compress(self):
        if self.simple_nifti.is_compressed:
            self.simple_nifti.uncompress()
        expected = str(self.simple_nifti.path) + ".gz"
        expected = Path(expected)
        result = self.simple_nifti.compress()
        self.assertEqual(result, expected)

    def test_uncompress(self):
        expected = str(self.simple_nifti.path).replace(".gz", "")
        expected = Path(expected)
        result = self.simple_nifti.uncompress()
        self.assertEqual(result, expected)

    def test_uncompress_already_uncompressed(self):
        if not self.simple_nifti.is_compressed:
            self.simple_nifti.compress()
        expected = str(self.simple_nifti.path).replace(".gz", "")
        expected = Path(expected)
        result = self.simple_nifti.uncompress()
        self.assertEqual(result, expected)

    ##############
    # Properties #
    ##############

    def test_b_value(self):
        result = self.dwi_nifti.b_value
        expected = self.dwi_nifti.get_b_value()
        self.assertEqual(result, expected)

    def test_b_value_for_non_DWI_returns_none(self):
        self.assertIsNone(self.simple_nifti.b_value)

    def test_b_vector(self):
        result = self.dwi_nifti.b_vector
        expected = self.dwi_nifti.get_b_vector()
        self.assertListEqual(result, expected)

    def test_b_vector_for_non_DWI_returns_none(self):
        self.assertIsNone(self.simple_nifti.b_vector)

    def test_compressed(self):
        expected = Path(self.simple_nifti.path)
        if not self.simple_nifti.is_compressed:
            expected = Path(str(expected) + ".gz")
        result = self.simple_nifti.compressed
        self.assertEqual(result, expected)

    def test_uncompressed(self):
        expected = Path(self.simple_nifti.path)
        if self.simple_nifti.is_compressed:
            expected = Path(str(expected).replace(".gz", ""))
        result = self.simple_nifti.uncompressed
        self.assertEqual(result, expected)
