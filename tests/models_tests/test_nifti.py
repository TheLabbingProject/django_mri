from datetime import datetime
from pathlib import Path

import factory
import numpy as np
import pytz
from django.db.models import signals
from django.test import TestCase
from django_dicom.models import Image

from django_mri.models.nifti import NIfTI
from django_mri.models.scan import Scan
from django_mri.models.session import Session
from tests.fixtures import (DICOM_MPRAGE_PATH, SIEMENS_DWI_SERIES,
                            SIEMENS_DWI_SERIES_PATH)
from tests.models import Subject


class NIfTIModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        # MPRAGE scan
        Image.objects.import_path(
            DICOM_MPRAGE_PATH, progressbar=False, report=False
        )
        series = Image.objects.first().series
        subject, _ = Subject.objects.from_dicom_patient(series.patient)
        header = series.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session = Session.objects.create(subject=subject, time=session_time)
        cls.simple_scan = Scan.objects.create(dicom=series, session=session)
        cls.simple_nifti = cls.simple_scan.nifti

        # DWI scan
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        series_dwi = Image.objects.last().series
        subject_dwi, _ = Subject.objects.from_dicom_patient(series_dwi.patient)
        header = series_dwi.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session, _ = Session.objects.get_or_create(
            subject=subject_dwi, time=session_time
        )
        cls.dwi_scan = Scan.objects.create(dicom=series_dwi, session=session)
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
        self.simple_nifti._resolve_compression_state()
        source = self.simple_nifti.compress()
        self.assertTrue(source.exists())
        expected = source.with_suffix("")
        result = self.simple_nifti.uncompress(keep_source=True)
        self.assertEqual(result, expected)
        self.assertTrue(expected.exists())
        self.assertTrue(source.exists())

    def test_compress_keep_source(self):
        self.simple_nifti._resolve_compression_state()
        source = self.simple_nifti.uncompress()
        self.assertTrue(source.exists())
        expected = source.with_suffix(source.suffix + ".gz")
        result = self.simple_nifti.compress(keep_source=True)
        self.assertEqual(result, expected)
        self.assertTrue(expected.exists())
        self.assertTrue(source.exists())

    def test_compress_already_compressed(self):
        self.simple_nifti._resolve_compression_state()
        if not self.simple_nifti.is_compressed:
            self.simple_nifti.compress()
        expected = str(self.simple_nifti.path)
        expected = Path(expected)
        result = self.simple_nifti.compress()
        self.assertEqual(result, expected)

    def test_compress(self):
        self.simple_nifti._resolve_compression_state()
        if self.simple_nifti.is_compressed:
            self.simple_nifti.uncompress()
        expected = str(self.simple_nifti.path) + ".gz"
        expected = Path(expected)
        result = self.simple_nifti.compress()
        self.assertEqual(result, expected)

    def test_uncompress(self):
        self.simple_nifti._resolve_compression_state()
        expected = str(self.simple_nifti.path).replace(".gz", "")
        expected = Path(expected)
        result = self.simple_nifti.uncompress()
        self.assertEqual(result, expected)

    def test_uncompress_already_uncompressed(self):
        self.simple_nifti._resolve_compression_state()
        if not self.simple_nifti.is_compressed:
            self.simple_nifti.compress()
        expected = str(self.simple_nifti.path).replace(".gz", "")
        expected = Path(expected)
        result = self.simple_nifti.uncompress()
        self.assertEqual(result, expected)

    def test_get_total_readout_time(self):
        expected = self.simple_nifti.json_data.get("TotalReadoutTime")
        result = self.simple_nifti.get_total_readout_time()
        self.assertEqual(result, expected)

    def test_get_effective_spacing(self):
        expected = self.simple_nifti.json_data.get("EffectiveEchoSpacing")
        result = self.simple_nifti.get_effective_spacing()
        self.assertEqual(result, expected)

    def test_get_phase_encoding_direction(self):
        expected = self.simple_nifti.json_data.get("PhaseEncodingDirection")
        result = self.simple_nifti.get_phase_encoding_direction()
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

    def test_json_data(self):
        expected = self.simple_nifti.read_json()
        result = self.simple_nifti.json_data
        self.assertEqual(result, expected)

    def test_json_data_if_not_none(self):
        expected = self.simple_nifti.read_json()
        self.simple_nifti._json_data = expected
        result = self.simple_nifti.json_data
        self.assertEqual(result, expected)
