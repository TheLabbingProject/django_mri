import factory

from django.db.models import signals
from django.test import TestCase
from django_mri.models import Scan
from django_dicom.models import Image
from django_mri.models.common_sequences import sequences
from django_mri.models.sequence_type import SequenceType
from tests.factories import SubjectFactory
from tests.fixtures import (
    DICOM_MPRAGE_PATH,
    SIEMENS_DWI_SERIES_PATH,
)
from pathlib import Path


class BidsTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        for sequence in sequences:
            SequenceType.objects.get_or_create(**sequence)
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
        self.simple_nifti = self.simple_scan.dicom_to_nifti()
        self.dwi_nifti = self.dwi_scan.dicom_to_nifti()

    def test_mprage_path_value(self):
        destination = self.simple_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.simple_nifti.path)
        self.assertEqual(result, expected)

    def test_dwi_path_value(self):
        destination = self.dwi_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.dwi_nifti.path)
        self.assertEqual(result, expected)

