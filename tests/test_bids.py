import factory
import shutil
from django.db.models import signals
from django.test import TestCase
from django_mri.models import Scan
from django_dicom.models import Image, Series
from django_mri.models.common_sequences import sequences
from django_mri.models.sequence_type import SequenceType
from tests.factories import SubjectFactory
from tests.fixtures import (
    DICOM_MPRAGE_PATH,
    DICOM_DWI_PATH,
    DICOM_FLAIR_PATH,
    DICOM_FMAP_PATH,
    DICOM_FMRI_BOLD_PATH,
    DICOM_FMRI_SBREF_PATH,
    DICOM_IREPI_PATH,
    IMPORTED_DIR,
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
        series_mprage = Series.objects.get(description__icontains="MPRAGE")
        Scan.objects.get_or_create(dicom=series_mprage, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_DWI_PATH))
        series_dwi = Series.objects.get(description__icontains="ep2d")
        Scan.objects.get_or_create(dicom=series_dwi, subject=cls.subject)
        # Image.objects.import_path(Path(DICOM_FMAP_PATH))
        # series_fmap = Image.objects.last().series
        # Scan.objects.get_or_create(dicom=series_fmap, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FLAIR_PATH))
        series_flair = Series.objects.get(description__icontains="FLAIR")
        Scan.objects.get_or_create(dicom=series_flair, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_FMRI_BOLD_PATH))
        series_fmri_bold = Series.objects.get(description__icontains="FMRI")
        Scan.objects.get_or_create(dicom=series_fmri_bold, subject=cls.subject)
        # Image.objects.import_path(Path(DICOM_FMRI_SBREF_PATH))
        # series_fmri_sbref = Image.objects.last().series
        # Scan.objects.get_or_create(dicom=series_fmri_sbref, subject=cls.subject)
        Image.objects.import_path(Path(DICOM_IREPI_PATH))
        series_irepi = Series.objects.get(description__icontains="IR-EPI")
        Scan.objects.get_or_create(dicom=series_irepi, subject=cls.subject)

        dwi = SequenceType.objects.get(title="DWI")
        mprage = SequenceType.objects.get(title="MPRAGE")
        irepi = SequenceType.objects.get(title="IR-EPI")
        flair = SequenceType.objects.get(title="FLAIR")
        fmri_bold = SequenceType.objects.get(title="fMRI")

        cls.dwi_scan = [
            scan for scan in Scan.objects.all() if scan.sequence_type == dwi
        ][0]
        cls.mprage_scan = [
            scan for scan in Scan.objects.all() if scan.sequence_type == mprage
        ][0]
        cls.flair_scan = [
            scan for scan in Scan.objects.all() if scan.sequence_type == flair
        ][0]
        cls.irepi_scan = [
            scan for scan in Scan.objects.all() if scan.sequence_type == irepi
        ][0]
        cls.fmri_bold_scan = [
            scan for scan in Scan.objects.all() if scan.sequence_type == fmri_bold
        ][0]

    # @classmethod
    # def tearDownClass(cls):
    #     for subdir in Path(IMPORTED_DIR).iterdir():
    #         shutil.rmtree(subdir)

    def setUp(self):
        # self.fmap_scan = Scan.objects.filter(description__icontains="PA").first()
        # self.fmri_sbref_scan = Scan.objects.filter(
        #     description__icontains="sbref"
        # ).first()

        self.mprage_nifti = self.mprage_scan.nifti
        self.dwi_nifti = self.dwi_scan.nifti
        self.flair_nifti = self.flair_scan.nifti
        self.irepi_nifti = self.irepi_scan.nifti
        # self.fmap_nifti = self.fmap_scan.nifti
        self.fmri_bold_nifti = self.fmri_bold_scan.nifti
        # self.fmri_sbref_nifti = self.fmri_sbref_scan.nifti

    def test_mprage_path_value(self):
        destination = self.mprage_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.mprage_nifti.path)
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

    # def test_fmap_path_value(self):
    #     destination = self.fmap_scan.get_bids_destination()
    #     expected = str(destination) + ".nii.gz"
    #     result = str(self.fmap_nifti.path)
    #     self.assertEqual(result, expected)

    def test_fmri_bold_path_value(self):
        destination = self.fmri_bold_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.fmri_bold_nifti.path)
        self.assertEqual(result, expected)

    # def test_fmri_sbref_path_value(self):
    #     destination = self.fmri_sbref_scan.get_bids_destination()
    #     expected = str(destination) + ".nii.gz"
    #     result = str(self.fmri_sbref_nifti.path)
    #     self.assertEqual(result, expected)
