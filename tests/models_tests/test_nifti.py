import factory
import numpy as np

from django.db.models import signals
from django.test import TestCase
from django_dicom.models import Image
from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from tests.utils import load_common_sequences
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
        load_common_sequences()
        cls.subject = SubjectFactory()

        # MPRAGE scan
        Image.objects.import_path(
            DICOM_MPRAGE_PATH, progressbar=False, report=False
        )
        series = Image.objects.first().series
        cls.simple_scan = Scan.objects.create(
            dicom=series, subject=cls.subject
        )
        cls.simple_nifti = cls.simple_scan.nifti

        # DWI scan
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        series_dwi = Image.objects.last().series
        cls.dwi_scan = Scan.objects.create(
            dicom=series_dwi, subject=cls.subject
        )
        cls.dwi_nifti = cls.dwi_scan.nifti

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
        destination = self.dwi_scan.get_bids_destination()
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
