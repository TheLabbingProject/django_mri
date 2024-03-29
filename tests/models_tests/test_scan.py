from datetime import datetime
from pathlib import Path

import factory
import pytz
from django.core.exceptions import ValidationError
from django.db.models import signals
from django.test import TestCase
from django_dicom.models import Image, Series
from django_mri.models import NIfTI, Scan, Session
from django_mri.utils import get_mri_root
from tests.fixtures import SIEMENS_DWI_SERIES, SIEMENS_DWI_SERIES_PATH
from tests.models import Subject


class ScanModelTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        Image.objects.import_path(
            SIEMENS_DWI_SERIES_PATH, progressbar=False, report=False
        )
        cls.series = Series.objects.first()
        cls.subject, _ = Subject.objects.from_dicom_patient(cls.series.patient)

    def setUp(self):
        header = self.series.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session, _ = Session.objects.get_or_create(
            subject=self.subject, time=session_time
        )
        self.scan = Scan.objects.create(dicom=self.series, session=session)

    ########
    # Meta #
    ########

    def test_unique_together(self):
        expected = (("number", "session"),)
        self.assertTupleEqual(Scan._meta.unique_together, expected)

    def test_ordering(self):
        self.assertTupleEqual(Scan._meta.ordering, ("-time",))

    def test_verbose_name_plural(self):
        self.assertTrue(Scan._meta.verbose_name_plural, "Scans")

    ##########
    # Fields #
    ##########

    # time
    def test_time_value(self):
        result = self.scan.time
        expected = SIEMENS_DWI_SERIES["time"]
        self.assertEqual(result, expected)

    def test_time_blank_and_null(self):
        field = Scan._meta.get_field("time")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # description
    def test_description_value(self):
        expected = SIEMENS_DWI_SERIES["description"]
        self.assertEqual(self.scan.description, expected)

    def test_description_blank_and_null(self):
        field = Scan._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_description_max_length(self):
        field = Scan._meta.get_field("description")
        self.assertEqual(field.max_length, 100)

    # number
    def test_number_value(self):
        expected = SIEMENS_DWI_SERIES["number"]
        self.assertEqual(self.scan.number, expected)

    def test_number_blank_and_null(self):
        field = Scan._meta.get_field("number")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_number_must_be_positive(self):
        invalid = [-100, -40, -1]
        for number in invalid:
            self.scan.number = number
            with self.assertRaises(ValidationError):
                self.scan.full_clean()

    # echo_time
    def test_echo_time_value(self):
        value = self.scan.echo_time
        expected = SIEMENS_DWI_SERIES["echo_time"]
        self.assertEqual(value, expected)

    def test_echo_time_blank_and_null(self):
        field = Scan._meta.get_field("echo_time")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_echo_time_must_be_positive(self):
        invalid = [-14.4, -40.8, -1]
        for number in invalid:
            self.scan.echo_time = number
            with self.assertRaises(ValidationError):
                self.scan.full_clean()

    # repetition_time
    def test_repetition_time_value(self):
        value = self.scan.repetition_time
        expected = SIEMENS_DWI_SERIES["repetition_time"]
        self.assertEqual(value, expected)

    def test_repetition_time_blank_and_null(self):
        field = Scan._meta.get_field("repetition_time")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_repetition_time_must_be_positive(self):
        invalid = [-14.4, -40.8, -1]
        for number in invalid:
            self.scan.repetition_time = number
            with self.assertRaises(ValidationError):
                self.scan.full_clean()

    # inversion_time
    def test_inversion_time_value(self):
        self.assertIsNone(self.scan.inversion_time)

    def test_inversion_time_blank_and_null(self):
        field = Scan._meta.get_field("inversion_time")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_inversion_time_must_be_positive(self):
        invalid = [-14.4, -40.8, -1]
        for number in invalid:
            self.scan.inversion_time = number
            with self.assertRaises(ValidationError):
                self.scan.full_clean()

    # spatial_resolution
    def test_spatial_resolution_value(self):
        result = self.scan.spatial_resolution
        expected = SIEMENS_DWI_SERIES["spatial_resolution"]
        self.assertEqual(result, expected)

    def test_spatial_resolution_blank_and_null(self):
        field = Scan._meta.get_field("spatial_resolution")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_spatial_resolution_size(self):
        field = Scan._meta.get_field("spatial_resolution")
        self.assertEqual(field.size, 3)

    # comments
    def test_comments_blank_and_null(self):
        field = Scan._meta.get_field("comments")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_comments_max_length(self):
        field = Scan._meta.get_field("comments")
        self.assertEqual(field.max_length, 1000)

    # dicom
    def test_dicom_blank_and_null(self):
        field = Scan._meta.get_field("dicom")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_dicom_verbose_name(self):
        field = Scan._meta.get_field("dicom")
        expected = "DICOM Series"
        self.assertEqual(field.verbose_name, expected)

    # is_updated_from_dicom
    def test_is_updated_from_dicom_default(self):
        field = Scan._meta.get_field("is_updated_from_dicom")
        self.assertFalse(field.default)

    # _nifti
    def test__nifti_blank_and_null(self):
        field = Scan._meta.get_field("_nifti")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # session_id
    def test_session_id_not_blank_and_not_null(self):
        field = Scan._meta.get_field("session_id")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    ###########
    # Methods #
    ###########

    def test_string(self):
        time = self.scan.time.strftime("%Y-%m-%d %H:%M:%S")
        description = self.scan.description
        expected = f"{description} from {time}"
        result = str(self.scan)
        self.assertEqual(result, expected)

    def test_update_fields_from_dicom_with_no_dicom_raises_attribute_error(
        self,
    ):
        self.scan.dicom = None
        with self.assertRaises(AttributeError):
            self.scan.update_fields_from_dicom()
        self.scan.dicom = self.series

    def test_get_spatial_resolution_from_dicom(self):
        result = self.scan.spatial_resolution
        expected = SIEMENS_DWI_SERIES["spatial_resolution"]
        self.assertTupleEqual(result, expected)

    # TODO: Add test for 2D scan with no "SliceThickness"
    # def test_get_spatial_resolution_from_dicom_without_slice_thickness(self):
    #     result = self.scan.spatial_resolution
    #     expected = TWO_DIM_TEST_SERIES["spatial_resolution"]
    #     self.assertListEqual(result, expected)

    def test_get_default_nifti_dir(self):
        result = self.scan.get_default_nifti_dir()
        scan_dir = str(self.scan.dicom.path)
        expected = Path(scan_dir.replace("DICOM", "NIfTI")).parent
        self.assertEqual(result, expected)

    def test_get_default_nifti_dir_without_dicom(self):
        self.scan.dicom = None
        result = self.scan.get_default_nifti_dir()
        expected = get_mri_root() / "NIfTI"
        self.assertEqual(result, expected)
        self.scan.dicom = self.series

    def test_default_nifti_name(self):
        name = self.scan.get_default_nifti_name()
        expected = str(self.scan.id)
        self.assertEqual(name, expected)

    def test_get_default_nifti_destination(self):
        result = self.scan.get_default_nifti_destination()
        directory = self.scan.get_default_nifti_dir()
        name = self.scan.get_default_nifti_name()
        expected = directory / name
        self.assertEqual(result, expected)

    def test_dicom_to_nifti_with_no_dicom_raises_attribute_error(self):
        self.scan.dicom = None
        with self.assertRaises(AttributeError):
            self.scan.dicom_to_nifti()
        self.scan.dicom = self.series

    def test__nifti_before_dicom_to_nifti(self):
        result = self.scan._nifti
        self.assertIsNone(result)

    ##############
    # Properties #
    ##############

    def test_sequence_type(self):
        self.assertEqual(self.scan.sequence_type, "dwi")

    def test_nifti_returns_nifti(self):
        self.scan.dicom = self.series
        result = self.scan.nifti
        self.assertIsInstance(result, NIfTI)
