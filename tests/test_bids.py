import factory, pytz

from django.db.models import signals
from django.test import TestCase
from django_mri.models import Scan, Session
from django_dicom.models import Image, Series
from django_mri.models.sequence_type import SequenceType
from tests.utils import load_common_sequences
from tests.fixtures import (
    DICOM_MPRAGE_PATH,
    DICOM_DWI_PATH,
    DICOM_FLAIR_PATH,
    DICOM_FMRI_BOLD_PATH,
    DICOM_IREPI_PATH,
)
from tests.models import Subject
from datetime import datetime


class BidsTestCase(TestCase):
    @classmethod
    @factory.django.mute_signals(signals.post_save)
    def setUpTestData(cls):
        load_common_sequences()

        Image.objects.import_path(
            DICOM_MPRAGE_PATH, progressbar=False, report=False
        )
        series_mprage = Series.objects.get(description__icontains="MPRAGE")
        subject_mprage, _ = Subject.objects.from_dicom_patient(
            series_mprage.patient
        )
        header = series_mprage.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session_mprage = Session.objects.create(
            subject=subject_mprage, time=session_time
        )
        Scan.objects.get_or_create(dicom=series_mprage, session=session_mprage)

        Image.objects.import_path(
            DICOM_DWI_PATH, progressbar=False, report=False
        )
        series_dwi = Series.objects.get(description__icontains="ep2d")
        subject_dwi, _ = Subject.objects.from_dicom_patient(series_dwi.patient)
        header = series_dwi.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session_dwi = Session.objects.create(
            subject=subject_dwi, time=session_time
        )
        Scan.objects.get_or_create(dicom=series_dwi, session=session_dwi)

        Image.objects.import_path(
            DICOM_FLAIR_PATH, progressbar=False, report=False
        )
        series_flair = Series.objects.get(description__icontains="FLAIR")
        subject_flair, _ = Subject.objects.from_dicom_patient(
            series_flair.patient
        )
        header = series_flair.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session_flair = Session.objects.create(
            subject=subject_flair, time=session_time
        )
        Scan.objects.get_or_create(dicom=series_flair, session=session_flair)

        Image.objects.import_path(
            DICOM_FMRI_BOLD_PATH, progressbar=False, report=False
        )
        series_fmri_bold = Series.objects.get(description__icontains="FMRI")
        subject_fmri_bold, _ = Subject.objects.from_dicom_patient(
            series_fmri_bold.patient
        )
        header = series_fmri_bold.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session_fmri_bold = Session.objects.create(
            subject=subject_fmri_bold, time=session_time
        )
        Scan.objects.get_or_create(
            dicom=series_fmri_bold, session=session_fmri_bold
        )

        Image.objects.import_path(
            DICOM_IREPI_PATH, progressbar=False, report=False
        )
        series_irepi = Series.objects.get(description__icontains="IR-EPI")
        subject_irepi, _ = Subject.objects.from_dicom_patient(
            series_irepi.patient
        )
        header = series_irepi.image_set.first().header.instance
        session_time = datetime.combine(
            header.get("StudyDate"), header.get("StudyTime")
        ).replace(tzinfo=pytz.UTC)
        session_irepi = Session.objects.create(
            subject=subject_irepi, time=session_time
        )
        Scan.objects.get_or_create(dicom=series_irepi, session=session_irepi)

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
            scan
            for scan in Scan.objects.all()
            if scan.sequence_type == fmri_bold
        ][0]

        cls.mprage_nifti = cls.mprage_scan.nifti
        cls.dwi_nifti = cls.dwi_scan.nifti
        cls.flair_nifti = cls.flair_scan.nifti
        cls.irepi_nifti = cls.irepi_scan.nifti
        cls.fmri_bold_nifti = cls.fmri_bold_scan.nifti

        # TODO: Add tests for fmap and sbref
        # Image.objects.import_path(Path(DICOM_FMRI_SBREF_PATH))
        # series_fmri_sbref = Image.objects.last().series
        # Scan.objects.get_or_create(
        # dicom=series_fmri_sbref, subject=cls.subject)
        # Image.objects.import_path(Path(DICOM_FMAP_PATH))
        # series_fmap = Image.objects.last().series
        # Scan.objects.get_or_create(dicom=series_fmap, subject=cls.subject)
        # self.fmap_nifti = self.fmap_scan.nifti
        # self.fmri_sbref_nifti = self.fmri_sbref_scan.nifti
        # self.fmap_scan = Scan.objects.filter(
        # description__icontains="PA").first()
        # self.fmri_sbref_scan = Scan.objects.filter(
        #     description__icontains="sbref"
        # ).first()

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

    def test_fmri_bold_path_value(self):
        destination = self.fmri_bold_scan.get_bids_destination()
        expected = str(destination) + ".nii.gz"
        result = str(self.fmri_bold_nifti.path)
        self.assertEqual(result, expected)

    # def test_fmap_path_value(self):
    #     destination = self.fmap_scan.get_bids_destination()
    #     expected = str(destination) + ".nii.gz"
    #     result = str(self.fmap_nifti.path)
    #     self.assertEqual(result, expected)

    # def test_fmri_sbref_path_value(self):
    #     destination = self.fmri_sbref_scan.get_bids_destination()
    #     expected = str(destination) + ".nii.gz"
    #     result = str(self.fmri_sbref_nifti.path)
    #     self.assertEqual(result, expected)
