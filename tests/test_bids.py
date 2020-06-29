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
    DICOM_FLAIR_PATH,
    DICOM_FMAP_PATH,
    DICOM_FMRI_BOLD_PATH,
    DICOM_FMRI_SBREF_PATH,
    DICOM_IREPI_PATH,
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
        series_mprage = Image.objects.first().series
        Scan.objects.get_or_create(dicom=series_mprage, subject=cls.subject)
        Image.objects.import_path(Path(SIEMENS_DWI_SERIES_PATH))
        series_dwi = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_dwi, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FMAP_PATH))
        series_fmap = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_fmap, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FLAIR_PATH))
        series_flair = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_flair, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FMRI_BOLD_PATH))
        series_fmri_bold = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_fmri_bold, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FMRI_SBREF_PATH))
        series_fmri_sbref = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_fmri_sbref, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_IREPI_PATH))
        series_irepi = Image.objects.last().series
        Scan.objects.get_or_create(dicom=series_irepi, subject=cls.subject)

    def setUp(self):
        self.mprage_scan = Scan.objects.filter(description__icontains="mprage").first()
        self.dwi_scan = Scan.objects.filter(description__icontains="dwi").first()
        self.flair_scan = Scan.objects.filter(description__icontains="flair").first()
        self.irepi_scan = Scan.objects.filter(description__icontains="ir-epi").first()
        self.fmap_scan = Scan.objects.filter(description__icontains="PA").first()
        self.fmri_bold_scan = Scan.objects.filter(description__icontains="bold").first()
        self.fmri_sbref_scan = Scan.objects.filter(
            description__icontains="sbref"
        ).first()

        self.mprage_nifti = self.mprage_scan.nifti
        self.dwi_nifti = self.dwi_scan.nifti
        self.flair_nifti = self.flair_scan.nifti
        self.irepi_nifti = self.irepi_scan.nifti
        self.fmap_nifti = self.fmap_scan.nifti
        self.fmri_bold_nifti = self.fmri_bold_scan.nifti
        self.fmri_sbref_nifti = self.fmri_sbref_scan.nifti

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

    def test_flair_path_value(self):
        destination = self.flair_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.flair_nifti.path)
        self.assertEqual(result, expected)

    def test_irepi_path_value(self):
        destination = self.irepi_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.irepi_nifti.path)
        self.assertEqual(result, expected)

    def test_fmap_path_value(self):
        destination = self.fmap_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.fmap_nifti.path)
        self.assertEqual(result, expected)

    def test_fmri_bold_path_value(self):
        destination = self.fmri_bold_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.fmri_bold_nifti.path)
        self.assertEqual(result, expected)

    def test_fmri_sbref_path_value(self):
        destination = self.fmri_sbref_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.fmri_sbref_nifti.path)
        self.assertEqual(result, expected)
